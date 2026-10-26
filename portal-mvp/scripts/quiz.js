/* ═══════════════════════════════════════════
   L&D без суеты — Quiz Logic
   Reads data-correct from .quiz-item, validates on submit
   ═══════════════════════════════════════════ */

(function(){
  document.querySelectorAll('.quiz').forEach(function(quiz){
    var items = quiz.querySelectorAll('.quiz-item');
    var btn = quiz.querySelector('.quiz-submit');
    var result = quiz.querySelector('.quiz-result');
    var done = false;

    if (!btn || !items.length) return;

    function resetState(){
      done = false;
      items.forEach(function(item){
        item.classList.remove('done');
        item.querySelectorAll('.quiz-option').forEach(function(opt){
          opt.classList.remove('correct', 'wrong');
        });
        item.querySelectorAll('input[type="radio"]').forEach(function(r){
          r.checked = false;
        });
        item.style.borderColor = '';
      });
      btn.textContent = 'Проверить';
      result.textContent = '';
      result.className = 'quiz-result';
    }

    btn.addEventListener('click', function(e){
      e.preventDefault();

      if (done) { resetState(); return; }

      var score = 0;
      var allAnswered = true;

      items.forEach(function(item){
        var correct = item.getAttribute('data-correct');
        var selected = item.querySelector('input[type="radio"]:checked');

        item.classList.add('done');

        if (!selected) {
          allAnswered = false;
          item.style.borderColor = 'var(--terracotta, #b05a2e)';
          return;
        }

        var label = selected.closest('.quiz-option');
        if (selected.value === correct) {
          score++;
          if (label) label.classList.add('correct');
        } else {
          if (label) label.classList.add('wrong');
          var correctLabel = item.querySelector('.quiz-option:nth-of-type(' + (parseInt(correct)+1) + ')');
          if (correctLabel) correctLabel.classList.add('correct');
        }
      });

      if (!allAnswered) {
        result.textContent = 'Ответьте на все вопросы';
        result.className = 'quiz-result fail';
        items.forEach(function(item){ item.classList.remove('done'); });
        return;
      }

      done = true;
      btn.textContent = 'Пройти заново';

      var pct = Math.round((score / items.length) * 100);
      if (pct >= 80) {
        result.textContent = score + ' из ' + items.length + ' — отлично!';
        result.className = 'quiz-result pass';
      } else if (pct >= 50) {
        result.textContent = score + ' из ' + items.length + ' — неплохо, перечитайте сложные места';
        result.className = 'quiz-result fail';
      } else {
        result.textContent = score + ' из ' + items.length + ' — стоит вернуться к материалу';
        result.className = 'quiz-result fail';
      }

      // Save to localStorage
      var quizId = quiz.getAttribute('data-quiz-id') || window.location.pathname;
      try {
        var storage = JSON.parse(localStorage.getItem('ld_quiz_results') || '{}');
        storage[quizId] = { score: score, total: items.length, date: new Date().toISOString() };
        localStorage.setItem('ld_quiz_results', JSON.stringify(storage));
      } catch(_){}
    });

    // Restore previous result hint
    var quizId = quiz.getAttribute('data-quiz-id') || window.location.pathname;
    try {
      var storage = JSON.parse(localStorage.getItem('ld_quiz_results') || '{}');
      if (storage[quizId]) {
        var hint = quiz.querySelector('.quiz-previous');
        if (hint) {
          hint.textContent = 'Ранее: ' + storage[quizId].score + ' из ' + storage[quizId].total;
          hint.style.display = 'block';
        }
      }
    } catch(_){}
  });
})();