function automatedScroller() {
  const ClientNavs = document.querySelectorAll(".NavBtn");
  const ClientSlides = document.querySelectorAll(".page-client-box");

  var ClientNavNav = function (manual) {
    ClientNavs.forEach((ClientNav) => {
      ClientNav.classList.remove("active")
    });

    ClientSlides.forEach((ClientSlide) => {
      ClientSlide.classList.remove("active")
    });

    ClientNavs[manual].classList.add("active");
    ClientSlides[manual].classList.add("active");
  }

  ClientNavs.forEach((ClientNav, i) => {
    ClientNav.addEventListener("click", () => {
      ClientNavNav(i);
    });
  });

  // Select the first element in the "ClientNavs" array as the starting point
  let currentIndex = 0;

  // Set the interval for how often the code should scroll to the next element
  const interval = 5000; // 5000 ms = 5 seconds

  // Use the setInterval function to repeatedly call the "ClientNavNav" function
  setInterval(() => {
    // Increment the current index and wrap around to 0 if it exceeds the length of the "ClientNavs" array
    currentIndex = (currentIndex + 1) % ClientNavs.length;

    // Call the "ClientNavNav" function with the current index
    ClientNavNav(currentIndex);
  }, interval);
}

function ShadowScroller() {
  // Navbar shadowHeader Scroller Section //
  const shadowHeader = document.querySelector("header");
  const shadowHeaderIcon = document.querySelector(".colored-bg-hidden");
  const shadowHeaderIconBlack = document.querySelector(".colored-bg-hidden-shadow");

  window.addEventListener("scroll", () => {
    const isScrolled = window.scrollY > 0;
    shadowHeader.classList.toggle("shadow", isScrolled);
    shadowHeaderIcon.classList.toggle("shadow", isScrolled);
    shadowHeaderIconBlack.classList.toggle("shadow", isScrolled);
  });
}

function BoxSliderContainer() {
  // Animation Scroll Section
  const swiperTwos = document.querySelectorAll(".inspiration-devtegration-box-info-navigation-set");
  const sliderTwos = document.querySelectorAll(".inspiration-devtegration-box-info-navigation-set-content");

  var slideNavTwo = function (manual) {
    swiperTwos.forEach((swiperTwo, index) => {
      swiperTwo.classList.remove("active");
      sliderTwos[index].classList.remove("active");
    });

    swiperTwos[manual].classList.add("active");
    sliderTwos[manual].classList.add("active");
  };

  // Automatically slide the slides every 3 seconds
  let currentSlide = 0;
  setInterval(() => {
    slideNavTwo(currentSlide);
    currentSlide = (currentSlide + 1) % swiperTwos.length;
  }, 8000);

  swiperTwos.forEach((swiperTwo, i) => {
    swiperTwo.addEventListener("click", () => {
      slideNavTwo(i);
    });
  });
}

function InspirationHeaderSlider() {
  // Animation Scroll Section
  const swiperTwos = document.querySelectorAll(".inspiration-devtegration-box-info-navigation-set");
  const sliderTwos = document.querySelectorAll(".inspiration-devtegration-box-info-navigation-set-content");

  var slideNavTwo = function (manual) {
    swiperTwos.forEach((swiperTwo, index) => {
      swiperTwo.classList.remove("active");
      sliderTwos[index].classList.remove("active");
    });

    swiperTwos[manual].classList.add("active");
    sliderTwos[manual].classList.add("active");
  };

  // Automatically slide the slides every 3 seconds
  let currentSlide = 0;
  setInterval(() => {
    slideNavTwo(currentSlide);
    currentSlide = (currentSlide + 1) % swiperTwos.length;
  }, 8000);

  swiperTwos.forEach((swiperTwo, i) => {
    swiperTwo.addEventListener("click", () => {
      slideNavTwo(i);
    });
  });
}


function InspirationHeaderSlider() {
  // Animation Scroll Section
  const InspirationSwipers = document.querySelectorAll(".inspiration-section-content");
  const InspirationSliders = document.querySelectorAll(".SwitcherBtn");

  var slideNavTwo = function (manual) {
    InspirationSwipers.forEach((InspirationSwiper, index) => {
      InspirationSwiper.classList.remove("active");
      InspirationSliders[index].classList.remove("active");
    });

    InspirationSwipers[manual].classList.add("active");
    InspirationSliders[manual].classList.add("active");
  };

  // Automatically slide the slides every 5 seconds
  let currentSlide = 0;
  setInterval(() => {
    slideNavTwo(currentSlide);
    currentSlide = (currentSlide + 1) % InspirationSwipers.length;
  }, 5000);

  InspirationSliders.forEach((InspirationSlider, i) => {
    InspirationSlider.addEventListener("click", () => {
      slideNavTwo(i);
      currentSlide = i;
    });
  });
}

function PartnerSlideFunction() {
  const TextSlides = document.querySelectorAll('.partner_page_header_redesign_container_content_details');
  const TextNavigationNumbers = document.querySelectorAll('.partner_page_header_redesign_navigation_input');
  let TextCurrentSlide = 0;

  function showSlide(index) {
    TextSlides[TextCurrentSlide].classList.remove('active');
    TextSlides[index].classList.add('active');
    TextNavigationNumbers[TextCurrentSlide].classList.remove('active');
    TextNavigationNumbers[index].classList.add('active');
    TextCurrentSlide = index;
  }

  function nextSlide() {
    const nextIndex = (TextCurrentSlide + 1) % TextSlides.length;
    showSlide(nextIndex);
  }

  function previousSlide() {
    const previousIndex = (TextCurrentSlide - 1 + TextSlides.length) % TextSlides.length;
    showSlide(previousIndex);
  }

  // Scroll to the first slide
  function scrollToFirstSlide() {
    showSlide(0);
    window.scrollTo(0, 0);
  }

  // Scroll to the last slide
  function scrollToLastSlide() {
    showSlide(TextSlides.length - 1);
    window.scrollTo(0, document.body.scrollHeight);
  }

  setInterval(nextSlide, 5000); // Change slide every 5 seconds
}

function NavigationResponsiveControl() {
  const DropMegaMenu = document.querySelector('.sm-navbar-icon');
  const CloseBtn = document.querySelector('.sm-navbar-icon-two');
  const NavigationMenuDrop = document.querySelector('.responsive-nav');

  DropMegaMenu.addEventListener('click', () => {
    DropMegaMenu.classList.toggle('active');
    CloseBtn.classList.toggle('active');
    NavigationMenuDrop.classList.toggle('active');
  });

  CloseBtn.addEventListener('click', () => {
    DropMegaMenu.classList.toggle('active');
    CloseBtn.classList.toggle('active');
    NavigationMenuDrop.classList.toggle('active');
  });
}

function OptionDropDownOne() {
  const MenuDropDowns = document.querySelectorAll(".DropDownBtn");
  MenuDropDowns.forEach((event) => {
    event.addEventListener("click", () => {
      if (event.classList.contains("active")) {
        event.classList.remove("active");
      } else {
        event.classList.add("active");
      }
    });
  });
}

function OptionDropDownTwo() {
  const MenuDropDownTwos = document.querySelectorAll(".DropDownBtnTwo");
  MenuDropDownTwos.forEach((event) => {
    event.addEventListener("click", () => {
      if (event.classList.contains("active")) {
        event.classList.remove("active");
      } else {
        event.classList.add("active");
      }
    });
  });
}

