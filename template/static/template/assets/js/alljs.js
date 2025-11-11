 document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelector('.slides');
    const slideElements = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.dot');
    
    let currentIndex = 0;
    const totalSlides = slideElements.length;
    
    // Go to specific slide
    function goToSlide(index) {
      currentIndex = index;
      updateSlider();
    }

    // Update slider position and active dot
    function updateSlider() {
      slides.style.transform = `translateX(-${currentIndex * 100}%)`;

      // Update active dot
      dots.forEach((dot, i) => {
        if (i === currentIndex) {
          dot.classList.add('active');
        } else {
          dot.classList.remove('active');
        }
      });
    }

    // Next slide
    function nextSlide() {
      currentIndex = (currentIndex + 1) % totalSlides;
      updateSlider();
    }

    // Add click event to dots
    dots.forEach((dot, index) => {
      dot.addEventListener('click', () => goToSlide(index));
    });
    
    // Set initial state
    updateSlider();
    
    // Auto-sliding functionality
    let interval = setInterval(nextSlide, 4000);

    // Mouse drag support
    let isDragging = false;
    let startX = 0;
    let currentX = 0;
    let dragOffset = 0;

    slides.addEventListener('mousedown', (e) => {
      isDragging = true;
      startX = e.pageX;
      slides.style.cursor = 'grabbing';
      clearInterval(interval);
    });

    slides.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      e.preventDefault();
      currentX = e.pageX;
      dragOffset = currentX - startX;
      const translateX = -currentIndex * 100 + (dragOffset / slides.offsetWidth) * 100;
      slides.style.transform = `translateX(${translateX}%)`;
    });

    slides.addEventListener('mouseup', (e) => {
      if (!isDragging) return;
      isDragging = false;
      slides.style.cursor = 'grab';
      
      const threshold = slides.offsetWidth * 0.2;
      
      if (dragOffset > threshold) {
        // Dragged right - go to previous
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
      } else if (dragOffset < -threshold) {
        // Dragged left - go to next
        currentIndex = (currentIndex + 1) % totalSlides;
      }
      
      updateSlider();
      interval = setInterval(nextSlide, 4000);
    });

    slides.addEventListener('mouseleave', () => {
      if (isDragging) {
        isDragging = false;
        slides.style.cursor = 'grab';
        updateSlider();
        interval = setInterval(nextSlide, 4000);
      }
    });

    // Touch support for mobile
    let touchStartX = 0;
    let touchEndX = 0;

    slides.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
      clearInterval(interval);
    });

    slides.addEventListener('touchmove', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      const touchOffset = touchEndX - touchStartX;
      const translateX = -currentIndex * 100 + (touchOffset / slides.offsetWidth) * 100;
      slides.style.transform = `translateX(${translateX}%)`;
    });

    slides.addEventListener('touchend', (e) => {
      const touchOffset = touchEndX - touchStartX;
      const threshold = slides.offsetWidth * 0.2;
      
      if (touchOffset > threshold) {
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
      } else if (touchOffset < -threshold) {
        currentIndex = (currentIndex + 1) % totalSlides;
      }
      
      updateSlider();
      interval = setInterval(nextSlide, 4000);
    });

    // Set cursor style
    slides.style.cursor = 'grab';
  });


  // Pause animation on hover
    const slider = document.querySelector('.animate-scroll');
    
    slider.addEventListener('mouseenter', () => {
        slider.style.animationPlayState = 'paused';
    });
    
    slider.addEventListener('mouseleave', () => {
        slider.style.animationPlayState = 'running';
    });


     document.addEventListener('DOMContentLoaded', function() {
        const slider = document.getElementById('slider');
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const slides = document.querySelectorAll('#slider > div');
        let currentIndex = 0;
        const totalSlides = slides.length;
        let autoplayInterval;
        
        // Function to check if we're on mobile
        function isMobile() {
          return window.innerWidth < 768; // md breakpoint in Tailwind
        }
        
        // Function to move the slider
        function updateSlider() {
          let slidePercentage;
          
          // If mobile, show one slide at a time (100%)
          // If desktop, show three slides at a time (33.33%)
          if (isMobile()) {
            slidePercentage = 100;
          } else {
            slidePercentage = 100 / 3;
          }
          
          const translateX = -currentIndex * slidePercentage;
          slider.style.transform = `translateX(${translateX}%)`;
        }
        
        // Function to go to next slide
        function nextSlide() {
          currentIndex++;
          
          // Reset to beginning when reaching the end
          if (isMobile()) {
            // For mobile: totalSlides is the max
            if (currentIndex >= totalSlides) {
              currentIndex = 0;
            }
          } else {
            // For desktop: totalSlides - 2 is the max (showing 3 at a time)
            if (currentIndex > totalSlides - 3) {
              currentIndex = 0;
            }
          }
          
          updateSlider();
        }
        
        // Function to go to previous slide
        function prevSlide() {
          currentIndex--;
          
          // Go to end when going before the first slide
          if (currentIndex < 0) {
            if (isMobile()) {
              currentIndex = totalSlides - 1;
            } else {
              currentIndex = totalSlides - 3;
            }
          }
          
          updateSlider();
        }
        
        // Start autoplay
        function startAutoplay() {
          autoplayInterval = setInterval(nextSlide, 5000);
        }
        
        // Stop autoplay
        function stopAutoplay() {
          clearInterval(autoplayInterval);
        }
        
        // Event listeners for buttons
        nextBtn.addEventListener('click', function() {
          stopAutoplay();
          nextSlide();
          startAutoplay();
        });
        
        prevBtn.addEventListener('click', function() {
          stopAutoplay();
          prevSlide();
          startAutoplay();
        });
        
        // Pause autoplay on hover
        slider.addEventListener('mouseenter', stopAutoplay);
        slider.addEventListener('mouseleave', startAutoplay);
        
        // Handle window resize
        window.addEventListener('resize', function() {
          // Reset to first slide and update the slider
          currentIndex = 0;
          updateSlider();
        });
        
        // Initialize slider
        updateSlider();
        startAutoplay();
      });


       document.addEventListener('DOMContentLoaded', function() {
            const video = document.getElementById('keeronVideo');
            const playButton = document.getElementById('playButton');
            const muteButton = document.getElementById('muteButton');
            const fullscreenButton = document.getElementById('fullscreenButton');
            const progressFill = document.getElementById('progressFill');
            const currentTimeElement = document.getElementById('currentTime');
            const durationElement = document.getElementById('duration');
            const videoContainer = document.querySelector('.video-container');
            
            // Set initial state
            let isPlaying = false;
            let isMuted = true;
            video.muted = true;
            
            // Function to format time in MM:SS format
            function formatTime(seconds) {
                const minutes = Math.floor(seconds / 60);
                seconds = Math.floor(seconds % 60);
                return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
            }
            
            // Update play/pause button UI
            function updatePlayButton() {
                playButton.innerHTML = isPlaying ? 
                    `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>` : 
                    `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>`;
            }
            
            // Update mute button UI
            function updateMuteButton() {
                muteButton.innerHTML = isMuted ? 
                    `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
                    </svg>` : 
                    `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
                    </svg>`;
            }
            
            // Play/Pause video
            playButton.addEventListener('click', function() {
                if (isPlaying) {
                    video.pause();
                } else {
                    video.play();
                }
                isPlaying = !isPlaying;
                updatePlayButton();
            });
            
            // Toggle mute
            muteButton.addEventListener('click', function() {
                video.muted = !video.muted;
                isMuted = video.muted;
                updateMuteButton();
            });
            
            // Fullscreen toggle
            fullscreenButton.addEventListener('click', function() {
                if (document.fullscreenElement) {
                    document.exitFullscreen();
                } else {
                    videoContainer.requestFullscreen();
                }
            });
            
            // Update progress bar as video plays
            video.addEventListener('timeupdate', function() {
                const progress = (video.currentTime / video.duration) * 100;
                progressFill.style.width = `${progress}%`;
                currentTimeElement.textContent = formatTime(video.currentTime);
            });
            
            // Set duration when metadata is loaded
            video.addEventListener('loadedmetadata', function() {
                durationElement.textContent = formatTime(video.duration);
            });
            
            // Click on progress bar to seek
            document.querySelector('.progress-bar').addEventListener('click', function(e) {
                const progressBar = this.getBoundingClientRect();
                const percent = (e.clientX - progressBar.left) / progressBar.width;
                video.currentTime = percent * video.duration;
            });
            
            // Handle video end
            video.addEventListener('ended', function() {
                isPlaying = false;
                updatePlayButton();
                video.currentTime = 0;
            });
            
            // Make the cards responsive on hover
            document.querySelectorAll('.feature-card').forEach(card => {
                card.addEventListener('mouseenter', function() {
                    this.classList.add('scale-105');
                });
                
                card.addEventListener('mouseleave', function() {
                    this.classList.remove('scale-105');
                });
            });
            
            // Set the video duration manually since we don't have a real video
            durationElement.textContent = '2:38';

            // Responsive adjustments
            function handleResize() {
                if (window.innerWidth < 768) {
                    // Mobile adjustments
                    document.querySelectorAll('.feature-card').forEach(card => {
                        card.classList.add('p-6');
                        card.classList.remove('p-8');
                    });
                } else {
                    // Desktop adjustments
                    document.querySelectorAll('.feature-card').forEach(card => {
                        card.classList.add('p-8');
                        card.classList.remove('p-6');
                    });
                }
            }
            
            // Initial call and event listener for window resize
            handleResize();
            window.addEventListener('resize', handleResize);
        });