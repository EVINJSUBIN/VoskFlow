// ═══════════════════════════════════════════════════
// VoskFlow — Commercial Grade Landing Page Scripts
// ═══════════════════════════════════════════════════

// Wait for DOM
document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') lucide.createIcons();

    // ── Theme Toggle ──────────────────────────────────
    const html = document.documentElement;
    const themeBtn = document.getElementById('theme-toggle');

    // Detect system preference or saved preference
    const savedTheme = localStorage.getItem('voskflow-theme');
    if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        html.classList.add('dark');
    } else {
        html.classList.remove('dark');
    }

    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            html.classList.toggle('dark');
            localStorage.setItem('voskflow-theme', html.classList.contains('dark') ? 'dark' : 'light');
        });
    }

    // ── Navbar Scroll Resize ──────────────────────────
    const navBar = document.getElementById('nav-bar');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const y = window.scrollY;
        if (navBar) {
            if (y > 30) {
                navBar.classList.add('scrolled');
            } else {
                navBar.classList.remove('scrolled');
            }
        }
        lastScroll = y;
    }, { passive: true });

    // ── Mobile Menu ───────────────────────────────────
    const mobileBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileBtn && mobileMenu) {
        mobileBtn.addEventListener('click', () => {
            const isHidden = mobileMenu.classList.contains('hidden');
            if (isHidden) {
                mobileMenu.classList.remove('hidden');
                requestAnimationFrame(() => {
                    mobileMenu.classList.add('open');
                });
            } else {
                mobileMenu.classList.remove('open');
                setTimeout(() => mobileMenu.classList.add('hidden'), 300);
            }
        });

        // Close on link click
        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.remove('open');
                setTimeout(() => mobileMenu.classList.add('hidden'), 300);
            });
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!mobileMenu.contains(e.target) && !mobileBtn.contains(e.target)) {
                mobileMenu.classList.remove('open');
                setTimeout(() => mobileMenu.classList.add('hidden'), 300);
            }
        });
    }

    // ── Interactive Dictation Simulator ───────────────
    const recordBtn = document.getElementById('record-btn');
    const btnText = document.getElementById('btn-text');
    const waveformContainer = document.getElementById('waveform-container');
    const outputSpan = document.getElementById('transcription-output');
    const editorBody = document.getElementById('editor-body');
    const statusDot = document.getElementById('status-dot');
    const statusLabel = document.getElementById('status-label');

    const phrases = [
        'def transcribe_audio(stream):',
        '    """Process audio frames offline with Vosk."""',
        '    model = VoskModel("en-us-0.22")',
        '    result = model.recognize(stream)',
        '    keyboard.write(result.text)',
        '    print(f"Typed {len(result.text.split())} words")',
    ];

    let lineCounter = 4;
    let phraseIndex = 0;
    let isRecording = false;
    let typingInterval = null;

    function simulateTyping(text, callback) {
        let i = 0;
        if (outputSpan) outputSpan.textContent = '';

        typingInterval = setInterval(() => {
            if (i < text.length) {
                if (outputSpan) outputSpan.textContent += text.charAt(i);
                i++;
                if (editorBody) editorBody.scrollTop = editorBody.scrollHeight;
            } else {
                clearInterval(typingInterval);
                if (callback) callback();
            }
        }, 45);
    }

    function startRecording() {
        if (isRecording) return;
        isRecording = true;

        if (recordBtn) {
            recordBtn.classList.add('recording');
            recordBtn.style.background = '#ef4444';
            recordBtn.style.color = '#fff';
        }
        if (btnText) btnText.textContent = 'Listening — release to type';
        if (waveformContainer) waveformContainer.style.opacity = '1';
        if (statusDot) { statusDot.style.background = '#ef4444'; statusDot.classList.add('animate-ping'); }
        if (statusLabel) statusLabel.textContent = 'recording';

        const phrase = phrases[phraseIndex];
        phraseIndex = (phraseIndex + 1) % phrases.length;
        simulateTyping(phrase);
    }

    function stopRecording() {
        if (!isRecording) return;
        isRecording = false;
        clearInterval(typingInterval);

        if (recordBtn) {
            recordBtn.classList.remove('recording');
            recordBtn.style.background = '';
            recordBtn.style.color = '';
        }
        if (btnText) btnText.textContent = 'Hold to Speak';
        if (waveformContainer) waveformContainer.style.opacity = '0.2';
        if (statusDot) { statusDot.style.background = '#22c55e'; statusDot.classList.remove('animate-ping'); }
        if (statusLabel) statusLabel.textContent = 'idle';

        if (outputSpan && editorBody) {
            const content = outputSpan.textContent;
            if (content.trim()) {
                const line = document.createElement('div');
                line.className = 'editor-line';
                line.innerHTML = `<span class="line-num">${lineCounter}</span><span class="line-content">${content}</span>`;
                const typingLine = document.getElementById('typing-line');
                if (typingLine) editorBody.insertBefore(line, typingLine);
                lineCounter++;
                const counterSpan = document.querySelector('#typing-line .line-num');
                if (counterSpan) counterSpan.textContent = lineCounter;
            }
            outputSpan.textContent = '';
            editorBody.scrollTop = editorBody.scrollHeight;
        }
    }

    if (recordBtn) {
        recordBtn.addEventListener('mousedown', startRecording);
        recordBtn.addEventListener('mouseup', stopRecording);
        recordBtn.addEventListener('mouseleave', stopRecording);
        recordBtn.addEventListener('touchstart', (e) => { e.preventDefault(); startRecording(); });
        recordBtn.addEventListener('touchend', (e) => { e.preventDefault(); stopRecording(); });
    }

    // Ctrl+Space hotkey
    let ctrlHeld = false;
    window.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.code === 'Space') {
            e.preventDefault();
            startRecording();
        }
    });
    window.addEventListener('keyup', (e) => {
        if (e.code === 'Space' || e.key === 'Control') {
            stopRecording();
        }
    });

    // ── Smooth Scroll for Anchor Links ────────────────
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
});
