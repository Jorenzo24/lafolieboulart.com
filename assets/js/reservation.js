/* La Folie Boulart — module de demande de réservation.
 *
 * Demande, et non réservation ferme : rien n'est confirmé à l'envoi.
 * Le séjour porte sur l'entièreté de la propriété, trois nuits minimum.
 */
(function () {
  'use strict';

  var root = document.querySelector('[data-resa]');
  if (!root) { return; }

  /* ------------------------------------------------------------------
   * Configuration
   * ------------------------------------------------------------------
   * ENDPOINT : URL qui reçoit la demande en POST (JSON).
   *   - sur le VPS : 'reservation.php' (script fourni à la racine)
   *   - service tiers : coller l'URL du formulaire
   * Laissé vide, le module bascule sur un envoi par messagerie.
   */
  var ENDPOINT = root.getAttribute('data-endpoint') || '';
  var MAILTO = root.getAttribute('data-mailto') || 'contact@lafolieboulart.com';
  var MIN_NIGHTS = 3;

  var MONTHS = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
                'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'];
  var DOW = ['L', 'M', 'M', 'J', 'V', 'S', 'D'];

  /* ---------- Utilitaires de dates ---------- */
  function startOfDay(d) { return new Date(d.getFullYear(), d.getMonth(), d.getDate()); }
  function addDays(d, n) { return new Date(d.getFullYear(), d.getMonth(), d.getDate() + n); }
  function sameDay(a, b) {
    return a && b && a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();
  }
  function nights(a, b) { return Math.round((b - a) / 86400000); }
  function iso(d) {
    var m = String(d.getMonth() + 1).padStart(2, '0');
    var j = String(d.getDate()).padStart(2, '0');
    return d.getFullYear() + '-' + m + '-' + j;
  }
  function human(d) {
    if (!d) { return '—'; }
    return d.getDate() + ' ' + MONTHS[d.getMonth()].toLowerCase() + ' ' + d.getFullYear();
  }

  /* ---------- État ---------- */
  var today = startOfDay(new Date());
  var view = new Date(today.getFullYear(), today.getMonth(), 1);
  var arrival = null;
  var departure = null;
  var step = 0;

  /* ------------------------------------------------------------------
   * Calendrier
   * ------------------------------------------------------------------ */
  var monthsWrap = root.querySelector('.cal__months');
  var btnPrev = root.querySelector('.cal__nav--prev');
  var btnNext = root.querySelector('.cal__nav--next');

  function monthHtml(base) {
    var y = base.getFullYear(), m = base.getMonth();
    var first = new Date(y, m, 1);
    // La semaine commence le lundi.
    var lead = (first.getDay() + 6) % 7;
    var total = new Date(y, m + 1, 0).getDate();

    var cells = '';
    for (var i = 0; i < lead; i++) {
      cells += '<span class="cal__day cal__day--empty" aria-hidden="true"></span>';
    }
    for (var day = 1; day <= total; day++) {
      var date = new Date(y, m, day);
      var past = date < today;
      var cls = 'cal__day';
      var pressed = 'false';

      if (arrival && departure) {
        if (date > arrival && date < departure) { cls += ' cal__day--in'; }
        if (sameDay(date, arrival)) { cls += ' cal__day--start'; pressed = 'true'; }
        if (sameDay(date, departure)) { cls += ' cal__day--end'; pressed = 'true'; }
      } else if (arrival && sameDay(date, arrival)) {
        cls += ' cal__day--start cal__day--end';
        pressed = 'true';
      }

      cells += '<button type="button" class="' + cls + '" data-date="' + iso(date) + '"' +
               (past ? ' disabled' : '') +
               ' aria-pressed="' + pressed + '"' +
               ' aria-label="' + human(date) + '">' + day + '</button>';
    }

    return '<div class="cal__month">' +
      '<p class="cal__title">' + MONTHS[m] + ' ' + y + '</p>' +
      '<div class="cal__dow" aria-hidden="true">' + DOW.map(function (d) { return '<span>' + d + '</span>'; }).join('') + '</div>' +
      '<div class="cal__days" role="grid">' + cells + '</div>' +
      '</div>';
  }

  function renderCal() {
    var second = new Date(view.getFullYear(), view.getMonth() + 1, 1);
    monthsWrap.innerHTML = monthHtml(view) + monthHtml(second);
    var atStart = view.getFullYear() === today.getFullYear() && view.getMonth() === today.getMonth();
    btnPrev.disabled = atStart;
    syncSummary();
  }

  monthsWrap.addEventListener('click', function (ev) {
    var cell = ev.target.closest('.cal__day');
    if (!cell || cell.disabled || cell.classList.contains('cal__day--empty')) { return; }
    var parts = cell.getAttribute('data-date').split('-');
    var picked = new Date(+parts[0], +parts[1] - 1, +parts[2]);

    if (!arrival || departure || picked <= arrival) {
      // premier clic, ou l'on recommence une sélection
      arrival = picked;
      departure = null;
    } else {
      if (nights(arrival, picked) < MIN_NIGHTS) {
        // On étend d'office au minimum exigé plutôt que de refuser le clic.
        departure = addDays(arrival, MIN_NIGHTS);
      } else {
        departure = picked;
      }
    }
    renderCal();
    clearError('dates');
  });

  btnPrev.addEventListener('click', function () {
    view = new Date(view.getFullYear(), view.getMonth() - 1, 1);
    renderCal();
  });
  btnNext.addEventListener('click', function () {
    view = new Date(view.getFullYear(), view.getMonth() + 1, 1);
    renderCal();
  });

  /* ------------------------------------------------------------------
   * Récapitulatif latéral
   * ------------------------------------------------------------------ */
  function syncSummary() {
    set('sum-arrival', human(arrival));
    set('sum-departure', human(departure));
    var n = (arrival && departure) ? nights(arrival, departure) : 0;
    set('sum-nights', n ? (n + (n > 1 ? ' nuits' : ' nuit')) : '—');
    var guests = val('adults');
    var kids = val('children');
    var g = guests ? guests + (guests > 1 ? ' adultes' : ' adulte') : '—';
    if (kids && +kids > 0) { g += ', ' + kids + (+kids > 1 ? ' enfants' : ' enfant'); }
    set('sum-guests', g);
  }

  function set(id, text) {
    var el = document.getElementById(id);
    if (el) { el.textContent = text; }
  }
  function val(name) {
    var el = root.querySelector('[name="' + name + '"]');
    return el ? el.value.trim() : '';
  }

  root.addEventListener('input', function (ev) {
    if (ev.target.name === 'adults' || ev.target.name === 'children') { syncSummary(); }
    if (ev.target.name) { clearError(ev.target.name); }
  });

  /* ------------------------------------------------------------------
   * Étapes
   * ------------------------------------------------------------------ */
  var panels = Array.prototype.slice.call(root.querySelectorAll('.resa__panel'));
  var stepItems = Array.prototype.slice.call(root.querySelectorAll('.steps__item'));

  function showStep(n) {
    step = n;
    panels.forEach(function (p, i) { p.classList.toggle('is-active', i === n); });
    stepItems.forEach(function (it, i) {
      it.setAttribute('data-state', i === n ? 'current' : (i < n ? 'done' : 'todo'));
    });
    if (n === 2) { buildReview(); }
    var top = root.getBoundingClientRect().top + window.scrollY - 110;
    window.scrollTo({ top: top, behavior: 'smooth' });
  }

  root.addEventListener('click', function (ev) {
    var next = ev.target.closest('[data-next]');
    var back = ev.target.closest('[data-back]');
    var goto = ev.target.closest('[data-goto]');
    if (next) { ev.preventDefault(); if (validate(step)) { showStep(step + 1); } }
    if (back) { ev.preventDefault(); showStep(Math.max(0, step - 1)); }
    if (goto) { ev.preventDefault(); showStep(+goto.getAttribute('data-goto')); }
  });

  /* ------------------------------------------------------------------
   * Validation
   * ------------------------------------------------------------------ */
  function showError(name, msg) {
    var box = root.querySelector('[data-error="' + name + '"]');
    var input = root.querySelector('[name="' + name + '"]');
    if (box) { box.textContent = msg; }
    if (input) { input.setAttribute('aria-invalid', 'true'); }
  }
  function clearError(name) {
    var box = root.querySelector('[data-error="' + name + '"]');
    var input = root.querySelector('[name="' + name + '"]');
    if (box) { box.textContent = ''; }
    if (input) { input.removeAttribute('aria-invalid'); }
  }

  function validate(n) {
    var ok = true;
    if (n === 0) {
      if (!arrival || !departure) {
        showError('dates', 'Merci de choisir une date d’arrivée et une date de départ.');
        ok = false;
      } else if (nights(arrival, departure) < MIN_NIGHTS) {
        showError('dates', 'Le séjour minimum est de ' + MIN_NIGHTS + ' nuits.');
        ok = false;
      }
      if (!val('adults') || +val('adults') < 1) {
        showError('adults', 'Indiquez au moins un adulte.');
        ok = false;
      }
    }
    if (n === 1) {
      [['firstname', 'Merci d’indiquer votre prénom.'],
       ['lastname', 'Merci d’indiquer votre nom.']].forEach(function (f) {
        if (!val(f[0])) { showError(f[0], f[1]); ok = false; }
      });
      var mail = val('email');
      if (!mail) {
        showError('email', 'Merci d’indiquer votre adresse e-mail.');
        ok = false;
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(mail)) {
        showError('email', 'Cette adresse e-mail semble incorrecte.');
        ok = false;
      }
    }
    if (!ok) {
      var bad = root.querySelector('[aria-invalid="true"]');
      if (bad) { bad.focus(); }
    }
    return ok;
  }

  /* ------------------------------------------------------------------
   * Récapitulatif avant envoi
   * ------------------------------------------------------------------ */
  function collect() {
    var n = (arrival && departure) ? nights(arrival, departure) : 0;
    return {
      arrivee: arrival ? iso(arrival) : '',
      depart: departure ? iso(departure) : '',
      nuits: n,
      adultes: val('adults'),
      enfants: val('children') || '0',
      occasion: val('occasion'),
      prenom: val('firstname'),
      nom: val('lastname'),
      email: val('email'),
      telephone: val('phone'),
      message: val('message')
    };
  }

  function buildReview() {
    var d = collect();
    var n = d.nuits;
    var guests = d.adultes + (d.adultes > 1 ? ' adultes' : ' adulte');
    if (+d.enfants > 0) { guests += ', ' + d.enfants + (+d.enfants > 1 ? ' enfants' : ' enfant'); }

    var sejour = [
      ['Arrivée', human(arrival)],
      ['Départ', human(departure)],
      ['Durée', n + (n > 1 ? ' nuits' : ' nuit')],
      ['Voyageurs', guests]
    ];
    if (d.occasion) { sejour.push(['Occasion', d.occasion]); }

    var coord = [
      ['Nom', d.prenom + ' ' + d.nom],
      ['E-mail', d.email]
    ];
    if (d.telephone) { coord.push(['Téléphone', d.telephone]); }

    function rows(list) {
      return list.map(function (r) {
        return '<div><dt>' + r[0] + '</dt><dd>' + escapeHtml(r[1]) + '</dd></div>';
      }).join('');
    }

    var html =
      '<div class="review__group">' +
        '<div class="review__head"><p class="review__name">Séjour</p>' +
        '<a class="review__edit" href="#" data-goto="0">Modifier</a></div>' +
        '<dl class="review__list">' + rows(sejour) + '</dl>' +
      '</div>' +
      '<div class="review__group">' +
        '<div class="review__head"><p class="review__name">Vos coordonnées</p>' +
        '<a class="review__edit" href="#" data-goto="1">Modifier</a></div>' +
        '<dl class="review__list">' + rows(coord) + '</dl>' +
      '</div>';

    if (d.message) {
      html += '<div class="review__group">' +
        '<div class="review__head"><p class="review__name">Votre message</p>' +
        '<a class="review__edit" href="#" data-goto="1">Modifier</a></div>' +
        '<p style="margin:0;font-size:15px;color:var(--ink-soft)">' + escapeHtml(d.message) + '</p>' +
      '</div>';
    }
    root.querySelector('[data-review]').innerHTML = html;
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  /* ------------------------------------------------------------------
   * Envoi
   * ------------------------------------------------------------------ */
  var form = root.querySelector('form');
  var submitBtn = root.querySelector('[data-submit]');

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    if (!validate(0) || !validate(1)) { return; }

    var consent = root.querySelector('[name="consent"]');
    if (consent && !consent.checked) {
      showError('consent', 'Merci d’accepter le traitement de vos données.');
      return;
    }
    // Champ piège : rempli, la soumission vient d'un robot.
    var trap = root.querySelector('[name="website"]');
    if (trap && trap.value) { return; }

    var data = collect();
    var label = submitBtn.querySelector('span');
    var initial = label.textContent;
    label.textContent = 'Envoi en cours…';
    submitBtn.disabled = true;

    if (!ENDPOINT) {
      // Sans service d'envoi configuré, on ouvre le message pré-rempli.
      window.location.href = mailtoLink(data);
      window.setTimeout(function () {
        label.textContent = initial;
        submitBtn.disabled = false;
        succeed(data);
      }, 700);
      return;
    }

    fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(data)
    }).then(function (r) {
      if (!r.ok) { throw new Error('HTTP ' + r.status); }
      succeed(data);
    }).catch(function () {
      label.textContent = initial;
      submitBtn.disabled = false;
      showError('consent',
        'L’envoi a échoué. Réessayez, ou écrivez-nous directement à ' + MAILTO + '.');
    });
  });

  function mailtoLink(d) {
    var lines = [
      'Demande de réservation — La Folie Boulart',
      '',
      'Arrivée : ' + human(arrival),
      'Départ : ' + human(departure),
      'Durée : ' + d.nuits + ' nuits',
      'Voyageurs : ' + d.adultes + ' adulte(s), ' + d.enfants + ' enfant(s)',
      d.occasion ? 'Occasion : ' + d.occasion : '',
      '',
      'Nom : ' + d.prenom + ' ' + d.nom,
      'E-mail : ' + d.email,
      d.telephone ? 'Téléphone : ' + d.telephone : '',
      '',
      d.message ? 'Message :' : '',
      d.message
    ].filter(function (l) { return l !== ''; });

    return 'mailto:' + MAILTO +
      '?subject=' + encodeURIComponent('Demande de réservation — ' + d.prenom + ' ' + d.nom) +
      '&body=' + encodeURIComponent(lines.join('\n'));
  }

  function succeed(d) {
    set('done-arrival', human(arrival));
    set('done-departure', human(departure));
    set('done-nights', d.nuits + (d.nuits > 1 ? ' nuits' : ' nuit'));
    set('done-email', d.email);
    showStep(3);
  }

  /* ---------- Départ ---------- */
  renderCal();
  showStep(0);
})();
