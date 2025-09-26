// ====== Toggle button setup ======
function setupToggle(groupId, single = true, defaultIndex = 0) {
  const group = document.getElementById(groupId);
  if (!group) return;
  const buttons = Array.from(group.querySelectorAll("button"));
  buttons.forEach((b, i) => {
    b.addEventListener("click", () => {
      if (single) {
        buttons.forEach(x => x.classList.remove("active"));
        b.classList.add("active");
      } else {
        b.classList.toggle("active");
      }
    });
  });
  if (buttons[defaultIndex]) buttons[defaultIndex].classList.add("active");
}

// เรียกใช้กับกลุ่มปุ่ม
setupToggle("gender-group", true, 0);
setupToggle("type-group", true, 0);
setupToggle("alc-group", true, 0);
setupToggle("helmet-group", true, 0);
setupToggle("phone-group", true, 0);

// ====== Helper Functions ======
function convertGCS(gcsSum) {
  if (gcsSum < 3) return 0;
  if (gcsSum <= 5) return 1;
  if (gcsSum <= 8) return 2;
  if (gcsSum <= 12) return 3;
  return 4;
}

function convertSBP(sbp) {
  if (sbp <= 0) return 0;
  if (sbp <= 49) return 1;
  if (sbp <= 75) return 2;
  if (sbp <= 89) return 3;
  return 4;
}

function convertRR(rr) {
  if (rr <= 0) return 0;
  if (rr <= 5) return 1;
  if (rr <= 9) return 2;
  if (rr >= 10 && rr <= 29) return 3;
  return 4;
}

function preprocessInputs(raw) {
  return {
    SEX: raw.gender === "ชาย" ? 1 : 2,
    AGE: parseInt(raw.age, 10),
    Injp: raw.injury === "เดินเท้า" ? 1 : raw.injury === "ผู้ขับขี่" ? 2 : 3,
    Risk1: raw.alcohol === "ดื่ม" ? 0 : raw.alcohol === "ไม่ดื่ม" ? 1 : 2,
    Risk4: raw.helmet === "ใช้" ? 0 : raw.helmet === "ไม่ใช้" ? 1 : 2,
    Risk5: raw.phone === "ใช้" ? 0 : raw.phone === "ไม่ใช้" ? 1 : 2,
    Ais1: parseInt(raw.ais1, 10),
    Ais2: parseInt(raw.ais2, 10),
    Ais3: parseInt(raw.ais3, 10),
    Ais4: parseInt(raw.ais4, 10),
    Ais5: parseInt(raw.ais5, 10),
    Ais6: parseInt(raw.ais6, 10),
    SBP: parseInt(raw.sbp, 10),
    RR: parseInt(raw.rr, 10),
    PR: parseInt(raw.pr, 10),
    GCS: raw.eye + raw.verbal + raw.motor,
    Time: parseInt(raw.time, 10),
  };
}

function computeISS() {
  const aisEls = document.querySelectorAll(".ais");
  let aisVals = Array.from(aisEls).map(el => Number(el.value) || 0);
  aisVals.sort((a, b) => b - a);
  let top3 = aisVals.slice(0, 3);
  return top3.reduce((sum, v) => sum + v * v, 0);
}

function computeRTS(gcsSum, sbp, rr) {
  const gcsCode = convertGCS(gcsSum);
  const sbpCode = convertSBP(sbp);
  const rrCode = convertRR(rr);

  const rts = (0.9368 * gcsCode) +
              (0.7326 * sbpCode) +
              (0.2908 * rrCode);

  return { rts: Number(rts.toFixed(2)), gcsCode, sbpCode, rrCode };
}

async function predictSurvival(inputs) {
  const response = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(inputs)
});
  const result = await response.json();
  return result.survivalProb; // ได้ค่าจริงจากโมเดล
}



function getStatusByRTS(rts) {
  if (rts <= 2) {
    return { text: "มีความรุนแรงมาก เสี่ยงต่อการเสียชีวิต", color: "red" };
  } else if (rts <= 4) {
    return { text: "ภาวะวิกฤตของชีวิต", color: "orange" };
  } else if (rts <= 6) {
    return { text: "ความรุนแรงปานกลาง", color: "yellow" };
  } else {
    return { text: "ความรุนแรงเล็กน้อย", color: "green" };
  }
}


function clearForm() {
  // รีค่า input ทั้งหมด
  document.querySelectorAll("input, select").forEach(el => {
    if (el.type === "number" || el.tagName === "SELECT") {
      el.value = "";
    }
  });
  document.querySelectorAll(".btn").forEach(btn => btn.classList.remove("active"));

  // เคลียร์ผลลัพธ์
  document.getElementById("surv").textContent = "-";
  document.getElementById("iss").textContent = "-";
  document.getElementById("rts").textContent = "-";
  document.getElementById("status-text").textContent = "-";
  document.getElementById("status-emoji").textContent = "—";
}


document.getElementById("predict").addEventListener("click", async () => {
  console.log("Predict button clicked ✅");

  // ====== ดึงค่าจากฟอร์ม ======
  const age = Number(document.getElementById("age").value);
  const sbp = Number(document.getElementById("sbp").value);
  const rr = Number(document.getElementById("rr").value);
  const pulse = Number(document.getElementById("pulse").value);
  const gcsEye = Number(document.getElementById("gcs-eye").value);
  const gcsVerbal = Number(document.getElementById("gcs-verbal").value);
  const gcsMotor = Number(document.getElementById("gcs-motor").value);
  const gcsSum = gcsEye + gcsVerbal + gcsMotor;

  const iss = computeISS();
  const rtsObj = computeRTS(gcsSum, sbp, rr);

  // ====== เตรียม payload ส่งไป Flask ======
  const payload = {
    AGE: age, SBP: sbp, RR: rr, PR: pulse,
    GCS: gcsSum, ISS: iss, RTS: rtsObj.rts,
    Time: Number(document.getElementById("time-min").value) || 0,
    SEX: 1, Injp: 1, Dead: 0,
    Ais1: 0, Ais2: 0, Ais3: 0, Ais4: 0, Ais5: 0, Ais6: 0,
    Risk1: 0, Risk4: 0, Risk5: 0
  };

  try {
    // ====== เรียก Flask API ======
    const survivalProb = await predictSurvival(payload);

    // ====== แสดงผลลัพธ์ ======
    document.getElementById("surv").textContent = survivalProb + " %";
    document.getElementById("iss").textContent = iss;
    document.getElementById("rts").textContent = rtsObj.rts;

    const status = getStatusByRTS(rtsObj.rts);
    document.getElementById("status-text").textContent = status.text;

    // ====== แสดงอิโมจิพร้อมสี ======
    const emojiEl = document.getElementById("status-emoji");
    emojiEl.textContent = "⬤";  // วงกลม
    emojiEl.style.color = status.color;

  } catch (err) {
    console.error("Prediction error:", err);
    document.getElementById("status-text").textContent = "❌ Error";
  }
});
