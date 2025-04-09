/**
* Template Name: Tempo
* Template URL: https://bootstrapmade.com/tempo-free-onepage-bootstrap-theme/
* Updated: Aug 07 2024 with Bootstrap v5.3.3
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function() {
  "use strict";

  /**
   * Apply .scrolled class to the body as the page is scrolled down
   */
  function toggleScrolled() {
    const selectBody = document.querySelector('body');
    const selectHeader = document.querySelector('#header');
    if (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top')) return;
    window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
  }

  document.addEventListener('scroll', toggleScrolled);
  window.addEventListener('load', toggleScrolled);

  /**
   * Mobile nav toggle
   */
  const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    mobileNavToggleBtn.classList.toggle('bi-list');
    mobileNavToggleBtn.classList.toggle('bi-x');
  }
  mobileNavToggleBtn.addEventListener('click', mobileNavToogle);

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navmenu a').forEach(navmenu => {
    navmenu.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });

  });

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
    navmenu.addEventListener('click', function(e) {
      e.preventDefault();
      this.parentNode.classList.toggle('active');
      this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
      e.stopImmediatePropagation();
    });
  });

  /**
   * Preloader
   */
  const preloader = document.querySelector('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove();
    });
  }

  /**
   * Scroll top button
   */
  let scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  scrollTop.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    AOS.init({
      duration: 600,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', aosInit);

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: '.glightbox'
  });

  /**
   * Init isotope layout and filters
   */
  document.querySelectorAll('.isotope-layout').forEach(function(isotopeItem) {
    let layout = isotopeItem.getAttribute('data-layout') ?? 'masonry';
    let filter = isotopeItem.getAttribute('data-default-filter') ?? '*';
    let sort = isotopeItem.getAttribute('data-sort') ?? 'original-order';

    let initIsotope;
    imagesLoaded(isotopeItem.querySelector('.isotope-container'), function() {
      initIsotope = new Isotope(isotopeItem.querySelector('.isotope-container'), {
        itemSelector: '.isotope-item',
        layoutMode: layout,
        filter: filter,
        sortBy: sort
      });
    });

    isotopeItem.querySelectorAll('.isotope-filters li').forEach(function(filters) {
      filters.addEventListener('click', function() {
        isotopeItem.querySelector('.isotope-filters .filter-active').classList.remove('filter-active');
        this.classList.add('filter-active');
        initIsotope.arrange({
          filter: this.getAttribute('data-filter')
        });
        if (typeof aosInit === 'function') {
          aosInit();
        }
      }, false);
    });

  });

  /**
   * Frequently Asked Questions Toggle
   */
  document.querySelectorAll('.faq-item h3, .faq-item .faq-toggle').forEach((faqItem) => {
    faqItem.addEventListener('click', () => {
      faqItem.parentNode.classList.toggle('faq-active');
    });
  });

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function(swiperElement) {
      let config = JSON.parse(
        swiperElement.querySelector(".swiper-config").innerHTML.trim()
      );

      if (swiperElement.classList.contains("swiper-tab")) {
        initSwiperWithCustomPagination(swiperElement, config);
      } else {
        new Swiper(swiperElement, config);
      }
    });
  }

  window.addEventListener("load", initSwiper);

  /**
   * Correct scrolling position upon page load for URLs containing hash links.
   */
  window.addEventListener('load', function(e) {
    if (window.location.hash) {
      if (document.querySelector(window.location.hash)) {
        setTimeout(() => {
          let section = document.querySelector(window.location.hash);
          let scrollMarginTop = getComputedStyle(section).scrollMarginTop;
          window.scrollTo({
            top: section.offsetTop - parseInt(scrollMarginTop),
            behavior: 'smooth'
          });
        }, 100);
      }
    }
  });

  /**
   * Navmenu Scrollspy
   */
  let navmenulinks = document.querySelectorAll('.navmenu a');

  function navmenuScrollspy() {
    navmenulinks.forEach(navmenulink => {
      if (!navmenulink.hash) return;
      let section = document.querySelector(navmenulink.hash);
      if (!section) return;
      let position = window.scrollY + 200;
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        document.querySelectorAll('.navmenu a.active').forEach(link => link.classList.remove('active'));
        navmenulink.classList.add('active');
      } else {
        navmenulink.classList.remove('active');
      }
    })
  }
  window.addEventListener('load', navmenuScrollspy);
  document.addEventListener('scroll', navmenuScrollspy);

})();



  /**
   * loader animation
   */

// Wait until DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  
  const form = document.getElementById("upload-form");
  const fileInput = document.getElementById("plant_image");
  const imagePreview = document.getElementById("image-preview");
  const removeBtn = document.querySelector(".remove-image");
  const loadingOverlay = document.getElementById("loading-overlay");
  const resultBox = document.getElementById("result-box");

  // Preview the uploaded image
  window.previewImage = function (event) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        imagePreview.src = e.target.result;
        removeBtn.style.display = "block";
      };
      reader.readAsDataURL(file);
    }
  };

  // Remove the uploaded image
  window.removeImage = function () {
    fileInput.value = "";
    imagePreview.src = "/static/default-image.png";  // Update path if needed
    removeBtn.style.display = "none";
  };

  // Close the result section
  window.closeResult = function () {
    if (resultBox) {
      resultBox.style.display = "none";
    }
  };

  // Show loader on form submit
  if (form) {
    form.addEventListener("submit", function () {
      loadingOverlay.style.display = "flex";
    });
  }

});



  /**
   * chatbot
   */
  document.addEventListener("DOMContentLoaded", function () {
    const chatForm = document.getElementById("chat-form");
    const messageInput = document.getElementById("user_message");
    const chatBox = document.getElementById("chat-box");
    const typingIndicator = document.getElementById("typing-indicator");
  
    let userName = "";
    let isNameAsked = true;
  
    if (!chatForm || !messageInput || !chatBox) {
        console.warn("Chatbot elements not found on this page.");
        return;
    }
  
    chatForm.onsubmit = function (e) {
        e.preventDefault();
        const userInput = messageInput.value.trim();
        if (!userInput) return;
  
        appendUserMessage(userInput);
        messageInput.value = "";
  
        if (isNameAsked) {
            userName = userInput;
            isNameAsked = false;
            appendBotMessage(`Nice to meet you, ${userName}! 🌾 How can I help you with farming today?`);
            return;
        }
  
        if (typingIndicator) typingIndicator.style.display = "block";
  
        fetch(chatForm.dataset.url, {
            method: "POST",
            headers: {
                "X-CSRFToken": chatForm.dataset.csrf,
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                user_message: userInput,
                user_name: userName
            })
        })
            .then(res => res.json())
            .then(data => {
                if (typingIndicator) typingIndicator.style.display = "none";
                appendBotMessage(data.bot_response);
            })
            .catch(err => {
                if (typingIndicator) typingIndicator.style.display = "none";
                appendBotMessage("Oops! Something went wrong. Please try again.");
                console.error("Chatbot error:", err);
            });
    };
  
    function appendUserMessage(message) {
        chatBox.innerHTML += `<div class='user-message'><span>${message}</span><i class="bi bi-person-circle icon"></i></div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    }
  
    function appendBotMessage(message) {
        chatBox.innerHTML += `<div class='bot-message'><i class="bi bi-robot icon"></i><span>${message}</span></div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    }
  });



/**
 * loader animation for Pest Identification
 */
// Wait until DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  
  const form = document.getElementById("pest-upload-form");
  const fileInput = document.getElementById("pest_image");
  const imagePreview = document.getElementById("pest-image-preview");
  const removeBtn = document.querySelector(".pest-remove-image");
  const loadingOverlay = document.getElementById("pest-loading-overlay");
  const resultBox = document.getElementById("pest-result-box");

  // Preview the uploaded pest image
  window.previewPestImage = function (event) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        imagePreview.src = e.target.result;
        removeBtn.style.display = "block";
      };
      reader.readAsDataURL(file);
    }
  };

  // Remove the uploaded pest image
  window.removePestImage = function () {
    fileInput.value = "";
    imagePreview.src = "/static/default-image.png";  // Change path if needed
    removeBtn.style.display = "none";
  };

  // Close the pest result section
  window.closePestResult = function () {
    if (resultBox) {
      resultBox.style.display = "none";
    }
  };

  // Show pest loader on form submit
  if (form) {
    form.addEventListener("submit", function () {
      loadingOverlay.style.display = "flex";
    });
  }

});


/**
 * loader animation for Plant Identification
 */

document.addEventListener("DOMContentLoaded", function () {

  const form = document.getElementById("upload-form");
  const fileInput = document.getElementById("plant_image");
  const imagePreview = document.getElementById("image-preview");
  const removeBtn = document.querySelector(".remove-image");
  const loadingOverlay = document.getElementById("loading-overlay");
  const resultBox = document.getElementById("result-box");

  // Preview the uploaded image
  window.previewImage = function (event) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        imagePreview.src = e.target.result;
        removeBtn.style.display = "block";
      };
      reader.readAsDataURL(file);
    }
  };

  // Remove the uploaded image
  window.removeImage = function () {
    fileInput.value = "";
    imagePreview.src = "/static/default-image.png"; // Update this path if needed
    removeBtn.style.display = "none";
  };

  // Close the result section
  window.closeResult = function () {
    if (resultBox) {
      resultBox.style.display = "none";
    }
  };

  // Show loader on form submit
  if (form) {
    form.addEventListener("submit", function () {
      loadingOverlay.style.display = "flex";
    });
  }

});
