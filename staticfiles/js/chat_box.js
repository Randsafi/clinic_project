  document.addEventListener('DOMContentLoaded', function () {
    // ==== مريض ====
    const patientBox = document.getElementById('patient-chat-box');
    const patientToggle = document.getElementById('patient-chat-toggle');
    const patientClose = patientBox?.querySelector('#chat-close');

    if (patientToggle && patientBox) {
      patientToggle.addEventListener('click', () => {
        patientBox.classList.toggle('d-none');
      });
    }

    if (patientClose && patientBox) {
      patientClose.addEventListener('click', () => {
        patientBox.classList.add('d-none');
      });
    }

    // ==== دكتور ====
    const doctorBox = document.getElementById('doctor-chat-box');
    const doctorToggle = document.getElementById('doctor-chat-toggle');
    const doctorClose = doctorBox?.querySelector('#chat-close');

    if (doctorToggle && doctorBox) {
      doctorToggle.addEventListener('click', () => {
        doctorBox.classList.toggle('d-none');
      });
    }

    if (doctorClose && doctorBox) {
      doctorClose.addEventListener('click', () => {
        doctorBox.classList.add('d-none');
      });
    }
  });