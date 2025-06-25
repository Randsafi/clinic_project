  //ask_question
  const stars = document.querySelectorAll('.star');
  const ratingInput = document.getElementById('evaluation');
  const emojiDiv = document.getElementById('emoji');

  const emojis = {
    1: '😡',  // غاضب
    2: '😕',  // متردد
    3: '😐',  // محايد
    4: '🙂',  // سعيد
    5: '😍'   // مبسوط جداً
  };

  stars.forEach((star, index) => {
    star.addEventListener('click', () => {
      const rating = index + 1;
      ratingInput.value = rating;

      stars.forEach(s => s.classList.remove('selected'));
      for (let i = 0; i < rating; i++) {
        stars[i].classList.add('selected');
      }
      
      emojiDiv.textContent = emojis[rating];
    });
});
const closeBtn = document.getElementById('chat-close');
closeBtn.addEventListener('click', () => {
  chatBox.classList.add('d-none');
});


//appointment 
$(function () {
    let bookedSlots = [];  // قائمة المواعيد المحجوزة بصيغة '2025-06-22 14:00'

    function getDisabledHoursForDate(dateStr) {
        const hours = [];

        bookedSlots.forEach(slot => {
            const [date, time] = slot.split(' ');
            if (date === dateStr) {
                const hour = parseInt(time.split(':')[0]);
                if (!hours.includes(hour)) hours.push(hour);
            }
        });

        return hours;
    }

    function setupDateTimePicker(disabledHours=[]) {
        $('#datetimepicker').datetimepicker('destroy');  // إعادة تهيئة
        $('#datetimepicker').datetimepicker({
            format: 'YYYY-MM-DD HH:mm',
            stepping: 60,
            disabledHours: disabledHours,
            icons: {
                time: 'far fa-clock',
                date: 'far fa-calendar-alt',
                up: 'fas fa-arrow-up',
                down: 'fas fa-arrow-down',
                previous: 'fas fa-chevron-left',
                next: 'fas fa-chevron-right',
                today: 'far fa-calendar-check',
                clear: 'far fa-trash-alt',
                close: 'fas fa-times'
            }
        });

        // لما المستخدم يغير التاريخ، نحدث الساعات المحجوزة لهذا اليوم
        $('#datetimepicker').on('change.datetimepicker', function (e) {
            const selectedDate = moment(e.date).format('YYYY-MM-DD');
            const disabledHours = getDisabledHoursForDate(selectedDate);
            setupDateTimePicker(disabledHours);
        });
    }

    $('#id_doctor').change(function () {
        const doctorId = $(this).val();
        if (!doctorId) return;

        fetch(`/appointments/booked/${doctorId}/`)
            .then(response => response.json())
            .then(data => {
                bookedSlots = data;
                setupDateTimePicker();
            });
    });

    // أول تحميل
    setupDateTimePicker();
});