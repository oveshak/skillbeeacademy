


      const searchBtn = document.getElementById('searchBtn');
      const searchInputContainer = document.getElementById('searchInputContainer');
      const searchInput = document.getElementById('searchInput');

      // Check if we're on mobile or desktop
      function isMobile() {
        return window.innerWidth < 768;
      }

      // Toggle search input visibility (only works on mobile)
      if (searchBtn) {
        searchBtn.addEventListener('click', () => {
          if (isMobile()) {
            searchInputContainer.classList.toggle('active');

            if (searchInputContainer.classList.contains('active')) {
              // Focus the input when shown
              setTimeout(() => {
                searchInput.focus();
              }, 300);
            }
          }
        });
      }

      // Close search when clicking outside
      document.addEventListener('click', (event) => {
        if (searchInputContainer.classList.contains('active') &&
          !searchBtn.contains(event.target) &&
          !searchInputContainer.contains(event.target)) {
          searchInputContainer.classList.remove('active');
        }
      });

      // Close search on window resize if switching to desktop
      window.addEventListener('resize', () => {
        if (!isMobile() && searchInputContainer.classList.contains('active')) {
          searchInputContainer.classList.remove('active');
        }
      });

      // Add event listener for escape key to close search
      document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && searchInputContainer.classList.contains('active')) {
          searchInputContainer.classList.remove('active');
        }
      });
  

      const toggleButton = document.getElementById('whatsapp-toggle');
      const chatWidget = document.querySelector('.fixed.bottom-24');
      
      // Hide chat widget initially
      chatWidget.style.display = 'none';
      
      toggleButton.addEventListener('click', () => {
        if (chatWidget.style.display === 'none') {
          chatWidget.style.display = 'block';
        } else {
          chatWidget.style.display = 'none';
        }
      });

      
      // Elements
      const phoneScreen = document.getElementById('phone-screen');
      const otpScreen = document.getElementById('otp-screen');
      const phoneInput = document.getElementById('phone-input');
      const continueBtn = document.getElementById('continue-btn');
      const displayNumber = document.getElementById('display-number');
      const submitBtn = document.getElementById('submit-btn');
      const changeNumber = document.getElementById('change-number');
      const otpInputs = [
        document.getElementById('otp-1'),
        document.getElementById('otp-2'),
        document.getElementById('otp-3'),
        document.getElementById('otp-4'),
        document.getElementById('otp-5')
      ];
      const timerElement = document.getElementById('timer');

      // Phone number validation and button activation
      phoneInput.addEventListener('input', function () {
        const phoneNumber = this.value.trim();
        // Check if phone number is valid (11 digits for Bangladesh)
        if (phoneNumber.length === 11 && /^\d+$/.test(phoneNumber)) {
          continueBtn.classList.remove('bg-gray-100', 'text-gray-400', 'cursor-not-allowed');
          continueBtn.classList.add('bg-[#0a2849]', 'text-white', 'cursor-pointer');
          continueBtn.disabled = false;
        } else {
          continueBtn.classList.add('bg-gray-100', 'text-gray-400', 'cursor-not-allowed');
          continueBtn.classList.remove('bg-blue-100', 'text-blue-600', 'cursor-pointer');
          continueBtn.disabled = true;
        }
      });

      // Continue button click handler
      continueBtn.addEventListener('click', function () {
        if (!this.disabled) {
          // Show the phone number in the OTP screen
          displayNumber.textContent = '+88' + phoneInput.value;
          // Hide phone screen, show OTP screen
          phoneScreen.classList.add('hidden');
          otpScreen.classList.remove('hidden');
          // Focus on first OTP input
          otpInputs[0].focus();
          // Start timer
          startTimer(114); // 1 minute and 54 seconds
        }
      });

      // OTP input functionality
      otpInputs.forEach((input, index) => {
        // Handle input
        input.addEventListener('input', function () {
          if (this.value) {
            this.classList.add('filled');
            // Move to next input
            if (index < otpInputs.length - 1) {
              otpInputs[index + 1].focus();
            }
          } else {
            this.classList.remove('filled');
          }

          // Check if all inputs are filled
          checkOtpCompletion();
        });

        // Handle backspace
        input.addEventListener('keydown', function (e) {
          if (e.key === 'Backspace' && !this.value && index > 0) {
            otpInputs[index - 1].focus();
          }
        });
      });

      // Function to check if OTP is complete
      function checkOtpCompletion() {
        const isComplete = otpInputs.every(input => input.value.length === 1);

        if (isComplete) {
          submitBtn.classList.remove('bg-gray-100', 'text-gray-400', 'cursor-not-allowed');
          submitBtn.classList.add('bg-blue-100', 'text-blue-600', 'cursor-pointer');
          submitBtn.disabled = false;
        } else {
          submitBtn.classList.add('bg-gray-100', 'text-gray-400', 'cursor-not-allowed');
          submitBtn.classList.remove('bg-blue-100', 'text-blue-600', 'cursor-pointer');
          submitBtn.disabled = true;
        }
      }

      // Submit button click handler
      submitBtn.addEventListener('click', function () {
        if (!this.disabled) {
          alert('OTP verification successful!');
          // You can redirect or show the next screen here
        }
      });

      // Change number link
      changeNumber.addEventListener('click', function (e) {
        e.preventDefault();
        otpScreen.classList.add('hidden');
        phoneScreen.classList.remove('hidden');
        // Reset OTP inputs
        otpInputs.forEach(input => {
          input.value = '';
          input.classList.remove('filled');
        });
        // Reset button
        submitBtn.classList.add('bg-gray-100', 'text-gray-400', 'cursor-not-allowed');
        submitBtn.classList.remove('bg-blue-100', 'text-blue-600', 'cursor-pointer');
        submitBtn.disabled = true;
      });

      // Timer function
      function startTimer(seconds) {
        let remainingSeconds = seconds;

        function updateTimer() {
          const minutes = Math.floor(remainingSeconds / 60);
          const seconds = remainingSeconds % 60;

          // Format as MM:SS
          timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

          if (remainingSeconds <= 0) {
            clearInterval(interval);
            // Enable resend button logic would go here
          } else {
            remainingSeconds--;
          }
        }

        // Initial call
        updateTimer();
        // Update every second
        const interval = setInterval(updateTimer, 1000);
      }
   
      // Alpine.js handles all the interactive functionality
      document.addEventListener('DOMContentLoaded', function () {
        // Any additional initialization if needed
      });

      // First, let's add a toggle function for mobile dropdown menus
      document.addEventListener('DOMContentLoaded', function () {
        // Find all dropdown headings in the footer
        const dropdownHeadings = document.querySelectorAll('.footer-dropdown-heading');

        // Add click event listener to each heading
        dropdownHeadings.forEach(heading => {
          heading.addEventListener('click', function () {
            // Toggle the 'active' class on the parent element
            this.parentElement.classList.toggle('active');

            // Find the dropdown content associated with this heading
            const dropdownContent = this.nextElementSibling;

            // Toggle display of dropdown content
            if (dropdownContent.style.maxHeight) {
              dropdownContent.style.maxHeight = null;
            } else {
              dropdownContent.style.maxHeight = dropdownContent.scrollHeight + "px";
            }
          });
        });
      });




  