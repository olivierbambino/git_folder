document.addEventListener("DOMContentLoaded", function() {
    loadArtworks();
    loadBlogPosts();
    loadEvents();
    setupContactForm();
});

function loadArtworks() {
    // Fetch artworks from the server and display them in the gallery
    fetch('/api/artworks')
        .then(response => response.json())
        .then(data => {
            const artworksContainer = document.getElementById('artworks');
            data.forEach(artwork => {
                const artworkElement = document.createElement('div');
                artworkElement.classList.add('artwork');
                artworkElement.innerHTML = `
                    <img src="${artwork.image}" alt="${artwork.title}">
                    <h3>${artwork.title}</h3>
                    <p>${artwork.description}</p>
                `;
                artworksContainer.appendChild(artworkElement);
            });
        });
}

function loadBlogPosts() {
    // Fetch blog posts from the server and display them in the blog section
    fetch('/api/blog-posts')
        .then(response => response.json())
        .then(data => {
            const blogPostsContainer = document.getElementById('blog-posts');
            data.forEach(post => {
                const postElement = document.createElement('div');
                postElement.classList.add('blog-post');
                postElement.innerHTML = `
                    <h3>${post.title}</h3>
                    <p>${post.content}</p>
                `;
                blogPostsContainer.appendChild(postElement);
            });
        });
}

function loadEvents() {
    // Fetch events from the server and display them in the events calendar
    fetch('/api/events')
        .then(response => response.json())
        .then(data => {
            const eventsCalendar = document.getElementById('events-calendar');
            data.forEach(event => {
                const eventElement = document.createElement('div');
                eventElement.classList.add('event');
                eventElement.innerHTML = `
                    <h3>${event.title}</h3>
                    <p>${event.date}</p>
                    <p>${event.description}</p>
                `;
                eventsCalendar.appendChild(eventElement);
            });
        });
}

function setupContactForm() {
    const contactForm = document.getElementById('contact-form');
    contactForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(contactForm);
        fetch('/api/contact', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            alert('Message sent successfully!');
            contactForm.reset();
        })
        .catch(error => {
            alert('Error sending message. Please try again.');
        });
    });
}
