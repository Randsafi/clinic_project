document.addEventListener('DOMContentLoaded', function() {
  // وظيفة لجلب قيمة CSRF من الكوكيز
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const csrftoken = getCookie("csrftoken");

  const chatBox = document.getElementById('chat-box');
  const toggleBtn = document.getElementById('chat-toggle');
  const closeBtn = document.getElementById('chat-close');

  toggleBtn.addEventListener('click', () => {
    chatBox.classList.toggle('d-none');
  });

  closeBtn.addEventListener('click', () => {
    chatBox.classList.add('d-none');
  });

  document.getElementById('chat-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);
    const questionInput = form.querySelector('input[name="question_text"], textarea[name="question_text"]');
    const questionText = questionInput.value;
    const doctorSelect = document.getElementById('doctor');

    formData.set('doctor', doctorSelect.value);  // Set doctor manually

    fetch("{% url 'ask_doctor_chat' %}", {
      method: "POST",
      headers: { "X-CSRFToken": form.querySelector('[name=csrfmiddlewaretoken]').value },
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        const msgContainer = document.querySelector('.chat-messages');
        const msg = document.createElement('div');
        msg.className = 'mb-2 p-2 border rounded';
        msg.innerHTML = `<p><strong>🧑‍🦰 You:</strong> ${questionText}</p><p class="text-warning mb-0">⏳ Waiting for reply...</p>`;
        msgContainer.prepend(msg);
        questionInput.value = '';
      }
    });
  });
});
