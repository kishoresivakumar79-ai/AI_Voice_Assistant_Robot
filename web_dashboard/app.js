document.addEventListener('DOMContentLoaded', () => {
    // UI Elements
    const canvas = document.getElementById('avatar-canvas');
    const commandForm = document.getElementById('command-form');
    const commandInput = document.getElementById('command-input');
    const micBtn = document.getElementById('mic-btn');
    const speakingText = document.getElementById('speaking-text');
    const voiceIndicator = document.getElementById('voice-indicator');
    const waveformBox = document.getElementById('waveform-box');
    const jarvisImg = document.getElementById('jarvis-img');
    const transcriptBody = document.getElementById('transcript-body');
    const ttsToggle = document.getElementById('tts-toggle');
    const clearBtn = document.getElementById('clear-btn');
    const presetBtns = document.querySelectorAll('.preset-btn');
    const avatarBtn1 = document.getElementById('avatar-btn-1');
    const avatarBtn2 = document.getElementById('avatar-btn-2');

    if (avatarBtn1 && avatarBtn2) {
        avatarBtn1.addEventListener('click', () => {
            jarvisImg.src = '/image/images.jpeg';
            avatarBtn1.classList.add('active');
            avatarBtn2.classList.remove('active');
        });
        avatarBtn2.addEventListener('click', () => {
            jarvisImg.src = '/image/images_1.jpeg';
            avatarBtn2.classList.add('active');
            avatarBtn1.classList.remove('active');
        });
    }

    // -------------------------------------------------------------
    // 1. Three.js 3D MARK 12 Robot Avatar Model & Lighting Scene
    // -------------------------------------------------------------
    let scene, camera, renderer;
    let mark12Group, headGroup, mouthMesh, eyeLeftLight, eyeRightLight, chestReactorLight;
    let leftArmGroup, rightArmGroup, leftLegGroup, rightLegGroup;
    let outerRing, particleSphere;

    // Animation State Parameters
    let robotState = 'IDLE'; // 'IDLE', 'TALKING', 'WALKING_FORWARD', 'WALKING_BACKWARD', 'TURNING_LEFT', 'TURNING_RIGHT', 'WAVING'
    let animTime = 0;

    function init3DScene() {
        const container = canvas.parentElement;
        const width = container.clientWidth || 400;
        const height = container.clientHeight || 350;

        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
        camera.position.set(0, 1, 14);

        renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
        renderer.setSize(width, height);
        renderer.setPixelRatio(window.devicePixelRatio);

        // Lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
        scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0x00f3ff, 1.2);
        dirLight.position.set(5, 10, 7);
        scene.add(dirLight);

        // Build 3D MARK 12 Robot Structure
        mark12Group = new THREE.Group();
        scene.add(mark12Group);

        const textureLoader = new THREE.TextureLoader();
        const armorTexture = textureLoader.load('/image/images.jpeg');

        const redMetalMat = new THREE.MeshStandardMaterial({
            color: 0x801015,
            metalness: 0.8,
            roughness: 0.3,
            map: armorTexture
        });

        const goldMetalMat = new THREE.MeshStandardMaterial({
            color: 0xcc9933,
            metalness: 0.9,
            roughness: 0.2
        });

        const darkMetalMat = new THREE.MeshStandardMaterial({
            color: 0x151a24,
            metalness: 0.9,
            roughness: 0.4
        });

        const glowingCyanMat = new THREE.MeshBasicMaterial({ color: 0x00f3ff });

        // --- TORSO ---
        const torsoGeo = new THREE.BoxGeometry(2.4, 3.2, 1.4);
        const torsoMesh = new THREE.Mesh(torsoGeo, redMetalMat);
        torsoMesh.position.y = 0.5;
        mark12Group.add(torsoMesh);

        // Chest Arc Reactor Core
        const reactorGeo = new THREE.CylinderGeometry(0.5, 0.5, 0.2, 32);
        const reactorMat = new THREE.MeshBasicMaterial({ color: 0x00f3ff });
        const reactorMesh = new THREE.Mesh(reactorGeo, reactorMat);
        reactorMesh.rotation.x = Math.PI / 2;
        reactorMesh.position.set(0, 1.0, 0.72);
        mark12Group.add(reactorMesh);

        chestReactorLight = new THREE.PointLight(0x00f3ff, 2.5, 8);
        chestReactorLight.position.set(0, 1.0, 0.8);
        mark12Group.add(chestReactorLight);

        // --- HEAD (WITH LIGHTING EYES & TALKING MOUTH) ---
        headGroup = new THREE.Group();
        headGroup.position.set(0, 2.6, 0);
        mark12Group.add(headGroup);

        const headHelmGeo = new THREE.BoxGeometry(1.6, 1.8, 1.5);
        const headHelmMesh = new THREE.Mesh(headHelmGeo, goldMetalMat);
        headGroup.add(headHelmMesh);

        // Glowing Eye Visor Lenses
        const eyeGeo = new THREE.BoxGeometry(0.35, 0.1, 0.1);
        const eyeLeftMesh = new THREE.Mesh(eyeGeo, glowingCyanMat);
        eyeLeftMesh.position.set(-0.4, 0.2, 0.76);
        headGroup.add(eyeLeftMesh);

        const eyeRightMesh = new THREE.Mesh(eyeGeo, glowingCyanMat);
        eyeRightMesh.position.set(0.4, 0.2, 0.76);
        headGroup.add(eyeRightMesh);

        eyeLeftLight = new THREE.PointLight(0x00f3ff, 1.5, 4);
        eyeLeftLight.position.set(-0.4, 0.2, 0.9);
        headGroup.add(eyeLeftLight);

        eyeRightLight = new THREE.PointLight(0x00f3ff, 1.5, 4);
        eyeRightLight.position.set(0.4, 0.2, 0.9);
        headGroup.add(eyeRightLight);

        // Talking Mouth Arc Visualizer ("Tom Method" Lighting)
        const mouthGeo = new THREE.BoxGeometry(0.7, 0.15, 0.1);
        const mouthMat = new THREE.MeshBasicMaterial({ color: 0x00f3ff });
        mouthMesh = new THREE.Mesh(mouthGeo, mouthMat);
        mouthMesh.position.set(0, -0.45, 0.76);
        headGroup.add(mouthMesh);

        // --- LEFT ARM ---
        leftArmGroup = new THREE.Group();
        leftArmGroup.position.set(-1.6, 1.8, 0);
        mark12Group.add(leftArmGroup);

        const armGeo = new THREE.CylinderGeometry(0.35, 0.25, 2.6, 16);
        const leftArmMesh = new THREE.Mesh(armGeo, redMetalMat);
        leftArmMesh.position.y = -1.1;
        leftArmGroup.add(leftArmMesh);

        // --- RIGHT ARM (FOR WAVING GESTURE) ---
        rightArmGroup = new THREE.Group();
        rightArmGroup.position.set(1.6, 1.8, 0);
        mark12Group.add(rightArmGroup);

        const rightArmMesh = new THREE.Mesh(armGeo, redMetalMat);
        rightArmMesh.position.y = -1.1;
        rightArmGroup.add(rightArmMesh);

        // --- LEFT LEG ---
        leftLegGroup = new THREE.Group();
        leftLegGroup.position.set(-0.7, -1.1, 0);
        mark12Group.add(leftLegGroup);

        const legGeo = new THREE.CylinderGeometry(0.4, 0.3, 3.2, 16);
        const leftLegMesh = new THREE.Mesh(legGeo, redMetalMat);
        leftLegMesh.position.y = -1.4;
        leftLegGroup.add(leftLegMesh);

        // --- RIGHT LEG ---
        rightLegGroup = new THREE.Group();
        rightLegGroup.position.set(0.7, -1.1, 0);
        mark12Group.add(rightLegGroup);

        const rightLegMesh = new THREE.Mesh(legGeo, redMetalMat);
        rightLegMesh.position.y = -1.4;
        rightLegGroup.add(rightLegMesh);

        // --- HOLOGRAM OUTER RINGS ---
        const ringGeo = new THREE.TorusGeometry(6.2, 0.04, 16, 100);
        const ringMat = new THREE.MeshBasicMaterial({ color: 0x00aaff, wireframe: true, transparent: true, opacity: 0.4 });
        outerRing = new THREE.Mesh(ringGeo, ringMat);
        outerRing.rotation.x = Math.PI / 3;
        scene.add(outerRing);

        window.addEventListener('resize', onWindowResize);
        animate();
    }

    function onWindowResize() {
        const container = canvas.parentElement;
        if (!container) return;
        const width = container.clientWidth;
        const height = container.clientHeight;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    }

    // -------------------------------------------------------------
    // 2. Dynamic Animation Loop & Action Controller
    // -------------------------------------------------------------
    function animate() {
        requestAnimationFrame(animate);
        animTime += 0.05;

        // Outer Ring Rotation
        if (outerRing) outerRing.rotation.z -= 0.005;

        // Base Idle Animation
        mark12Group.position.y = Math.sin(animTime * 1.5) * 0.15;
        headGroup.rotation.y = Math.sin(animTime * 0.8) * 0.08;

        if (robotState === 'TALKING') {
            // "Tom Method" Speech Lighting & Mouth Shape Oscillations
            const pulse = (Math.sin(animTime * 15) + 1) / 2;
            mouthMesh.scale.set(1 + pulse * 0.8, 1 + pulse * 1.5, 1);
            mouthMesh.material.color.setHex(pulse > 0.5 ? 0x00ffff : 0x0088ff);
            eyeLeftLight.intensity = 2.5 + pulse * 2.0;
            eyeRightLight.intensity = 2.5 + pulse * 2.0;
            headGroup.rotation.x = Math.sin(animTime * 4) * 0.05;
        } else {
            mouthMesh.scale.set(1, 1, 1);
            mouthMesh.material.color.setHex(0x00f3ff);
            eyeLeftLight.intensity = 1.5;
            eyeRightLight.intensity = 1.5;
            headGroup.rotation.x = 0;
        }

        // Directional & Gesture Joint Pivot Animations
        if (robotState === 'WALKING_FORWARD') {
            const legSwing = Math.sin(animTime * 6) * 0.4;
            leftLegGroup.rotation.x = legSwing;
            rightLegGroup.rotation.x = -legSwing;
            leftArmGroup.rotation.x = -legSwing * 0.6;
            rightArmGroup.rotation.x = legSwing * 0.6;
            mark12Group.position.z = Math.sin(animTime * 3) * 0.4;
        } else if (robotState === 'WALKING_BACKWARD') {
            const legSwing = Math.sin(animTime * 6) * 0.4;
            leftLegGroup.rotation.x = -legSwing;
            rightLegGroup.rotation.x = legSwing;
            leftArmGroup.rotation.x = legSwing * 0.6;
            rightArmGroup.rotation.x = -legSwing * 0.6;
            mark12Group.position.z = -Math.sin(animTime * 3) * 0.4;
        } else if (robotState === 'TURNING_LEFT') {
            mark12Group.rotation.y = Math.PI / 4;
            headGroup.rotation.y = -Math.PI / 6;
            leftArmGroup.rotation.z = 0.3;
        } else if (robotState === 'TURNING_RIGHT') {
            mark12Group.rotation.y = -Math.PI / 4;
            headGroup.rotation.y = Math.PI / 6;
            rightArmGroup.rotation.z = -0.3;
        } else if (robotState === 'WAVING') {
            rightArmGroup.rotation.z = Math.PI - 0.5;
            rightArmGroup.rotation.x = Math.sin(animTime * 8) * 0.3;
        } else {
            // Reset to Neutral Stance
            leftLegGroup.rotation.x = 0;
            rightLegGroup.rotation.x = 0;
            leftArmGroup.rotation.x = 0;
            leftArmGroup.rotation.z = 0;
            rightArmGroup.rotation.x = 0;
            rightArmGroup.rotation.z = 0;
            mark12Group.rotation.y = 0;
        }

        renderer.render(scene, camera);
    }

    init3DScene();

    // -------------------------------------------------------------
    // 3. Command Processing & API Request Handler
    // -------------------------------------------------------------
    commandForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const text = commandInput.value.trim();
        if (text) {
            sendUserCommand(text);
            commandInput.value = '';
        }
    });

    presetBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const cmd = btn.getAttribute('data-cmd');
            if (cmd) sendUserCommand(cmd);
        });
    });

    clearBtn.addEventListener('click', () => {
        transcriptBody.innerHTML = '';
        addTranscript('SYSTEM', 'Console transcript cleared.', 'system-msg');
    });

    function sendUserCommand(commandText) {
        addTranscript('USER', commandText, 'user');
        setAssistantSpeakingState(true, "MARK 12 Processing...");

        fetch('/api/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: commandText })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                const responseText = data.response;
                const action = data.parsed_command ? data.parsed_command.action : 'none';
                
                // Trigger specific 3D Robot Limb Action
                triggerRobotAction(action);

                addTranscript('MARK 12', responseText, 'bot');
                speakingText.textContent = `"${responseText}"`;

                // Speak out loud if Voice Output is checked
                if (ttsToggle.checked) {
                    speakOutLoud(responseText);
                } else {
                    setTimeout(() => setAssistantSpeakingState(false), 3000);
                }
            } else {
                addTranscript('ERROR', data.message || 'Error processing command', 'system-msg');
                setAssistantSpeakingState(false);
            }
        })
        .catch(err => {
            console.error(err);
            addTranscript('ERROR', 'Failed to connect to backend AI server', 'system-msg');
            setAssistantSpeakingState(false);
        });
    }

    function triggerRobotAction(action) {
        if (action === 'move_forward') {
            robotState = 'WALKING_FORWARD';
            setTimeout(() => { if (robotState === 'WALKING_FORWARD') robotState = 'IDLE'; }, 4000);
        } else if (action === 'move_backward') {
            robotState = 'WALKING_BACKWARD';
            setTimeout(() => { if (robotState === 'WALKING_BACKWARD') robotState = 'IDLE'; }, 4000);
        } else if (action === 'turn_left') {
            robotState = 'TURNING_LEFT';
            setTimeout(() => { if (robotState === 'TURNING_LEFT') robotState = 'IDLE'; }, 4000);
        } else if (action === 'turn_right') {
            robotState = 'TURNING_RIGHT';
            setTimeout(() => { if (robotState === 'TURNING_RIGHT') robotState = 'IDLE'; }, 4000);
        } else if (action === 'wave_hand') {
            robotState = 'WAVING';
            setTimeout(() => { if (robotState === 'WAVING') robotState = 'IDLE'; }, 4000);
        } else if (action === 'stop') {
            robotState = 'IDLE';
        }
    }

    // -------------------------------------------------------------
    // 4. Web Speech API (Speech-to-Text & Text-to-Speech)
    // -------------------------------------------------------------
    function speakOutLoud(text) {
        if (!('speechSynthesis' in window)) {
            setAssistantSpeakingState(false);
            return;
        }

        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;

        utterance.onstart = () => {
            setAssistantSpeakingState(true, "MARK 12 Speaking...");
        };

        utterance.onend = () => {
            setAssistantSpeakingState(false);
        };

        utterance.onerror = () => {
            setAssistantSpeakingState(false);
        };

        window.speechSynthesis.speak(utterance);
    }

    // Speech Recognition (Mic Input)
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = () => {
            micBtn.classList.add('listening');
            commandInput.placeholder = "Listening... Speak your command now";
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            commandInput.value = transcript;
            sendUserCommand(transcript);
        };

        recognition.onerror = (event) => {
            console.warn("Speech recognition error:", event.error);
            micBtn.classList.remove('listening');
            commandInput.placeholder = "Type command...";
        };

        recognition.onend = () => {
            micBtn.classList.remove('listening');
            commandInput.placeholder = "Type command (e.g. 'Mark 12 move forward', 'move backward', 'turn left', 'turn right', 'wave hand')...";
        };

        micBtn.addEventListener('click', () => {
            try {
                recognition.start();
            } catch (e) {
                recognition.stop();
            }
        });
    } else {
        micBtn.style.opacity = '0.5';
        micBtn.title = "Speech recognition not supported in browser. Use text input.";
    }

    // -------------------------------------------------------------
    // 5. UI Helper Functions
    // -------------------------------------------------------------
    function setAssistantSpeakingState(isSpeaking, statusMsg) {
        if (isSpeaking) {
            voiceIndicator.classList.add('speaking');
            voiceIndicator.innerHTML = `<i class="fa-solid fa-volume-high"></i> ${statusMsg || 'SPEAKING'}`;
            waveformBox.classList.add('active');
            jarvisImg.classList.add('talking');
            if (robotState === 'IDLE') robotState = 'TALKING';
        } else {
            voiceIndicator.classList.remove('speaking');
            voiceIndicator.innerHTML = `<i class="fa-solid fa-circle"></i> STANDBY`;
            waveformBox.classList.remove('active');
            jarvisImg.classList.remove('talking');
            if (robotState === 'TALKING') robotState = 'IDLE';
        }
    }

    function addTranscript(sender, text, typeClass) {
        const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        const div = document.createElement('div');
        div.className = `log-entry ${typeClass}`;
        div.innerHTML = `<span class="time">[${timeStr}] ${sender}:</span> <span class="text">${escapeHtml(text)}</span>`;
        transcriptBody.appendChild(div);
        transcriptBody.scrollTop = transcriptBody.scrollHeight;
    }

    function escapeHtml(str) {
        return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }
});
