/**
 * TRANS-GEST — Three.js Luxury Particle Animation
 * Premium background with gold and emerald floating particles
 */
(function () {
    const canvas = document.getElementById('three-canvas');
    if (!canvas || typeof THREE === 'undefined') return;

    // --- Scene Setup ---
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 50;

    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setClearColor(0x000000, 0);

    // --- Particles ---
    const PARTICLE_COUNT = 1200;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(PARTICLE_COUNT * 3);
    const colors = new Float32Array(PARTICLE_COUNT * 3);
    const sizes = new Float32Array(PARTICLE_COUNT);
    const speeds = new Float32Array(PARTICLE_COUNT);

    const palette = [
        new THREE.Color(0xC9A84C),  // gold
        new THREE.Color(0xE2C97E),  // light gold
        new THREE.Color(0xA07C2A),  // deep gold
        new THREE.Color(0x2D8B6F),  // emerald
        new THREE.Color(0x3DAF8C),  // light emerald
    ];

    for (let i = 0; i < PARTICLE_COUNT; i++) {
        const i3 = i * 3;
        positions[i3] = (Math.random() - 0.5) * 130;
        positions[i3 + 1] = (Math.random() - 0.5) * 90;
        positions[i3 + 2] = (Math.random() - 0.5) * 70;

        const color = palette[Math.floor(Math.random() * palette.length)];
        colors[i3] = color.r;
        colors[i3 + 1] = color.g;
        colors[i3 + 2] = color.b;

        sizes[i] = Math.random() * 2.2 + 0.4;
        speeds[i] = Math.random() * 0.25 + 0.08;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

    const material = new THREE.PointsMaterial({
        size: 1.4,
        vertexColors: true,
        transparent: true,
        opacity: 0.6,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);

    // --- Mouse Tracking ---
    const mouse = { x: 0, y: 0, targetX: 0, targetY: 0 };

    document.addEventListener('mousemove', function (e) {
        mouse.targetX = (e.clientX / window.innerWidth - 0.5) * 2;
        mouse.targetY = -(e.clientY / window.innerHeight - 0.5) * 2;
    });

    // --- Animation ---
    let time = 0;

    function animate() {
        requestAnimationFrame(animate);
        time += 0.002;

        // Smooth mouse follow
        mouse.x += (mouse.targetX - mouse.x) * 0.04;
        mouse.y += (mouse.targetY - mouse.y) * 0.04;

        // Rotate particles based on mouse
        particles.rotation.x = mouse.y * 0.25 + time * 0.06;
        particles.rotation.y = mouse.x * 0.25 + time * 0.09;

        // Animate individual particles
        const pos = geometry.attributes.position.array;
        for (let i = 0; i < PARTICLE_COUNT; i++) {
            const i3 = i * 3;
            pos[i3 + 1] += Math.sin(time * speeds[i] * 4 + i) * 0.012;
            pos[i3] += Math.cos(time * speeds[i] * 2.5 + i * 0.5) * 0.006;
        }
        geometry.attributes.position.needsUpdate = true;

        renderer.render(scene, camera);
    }

    animate();

    // --- Resize ---
    window.addEventListener('resize', function () {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
})();
