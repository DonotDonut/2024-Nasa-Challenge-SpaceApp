function switchContent() {
    let introContent1 = document.getElementById('intro_Content1');
    let introContent2 = document.getElementById('intro_Content2');
    let button = document.getElementById('switchButton');

    // Check if intro_Content1 is visible
    if (introContent1.classList.contains('visible')) {
        // Hide intro_Content1, show intro_Content2
        introContent1.classList.remove('visible');
        introContent1.classList.add('hidden');
        
        introContent2.classList.remove('hidden');
        introContent2.classList.add('visible');
        
        // Update button text
        button.textContent = "Show Intro Content 1";
    } else {
        // Hide intro_Content2, show intro_Content1
        introContent2.classList.remove('visible');
        introContent2.classList.add('hidden');
        
        introContent1.classList.remove('hidden');
        introContent1.classList.add('visible');
        
        // Update button text
        button.textContent = "Show Intro Content 2";
    }
}
