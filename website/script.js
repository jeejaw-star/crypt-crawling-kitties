document.addEventListener('DOMContentLoaded', (event) => {
    const displayArea = document.getElementById('displayArea');
    
    // 1. Load posts when the page loads
    loadPosts();

    function loadPosts() {
        // Retrieve posts from localStorage, or start with an empty array if none exist
        const posts = JSON.parse(localStorage.getItem('forumPosts')) || [];
        displayArea.innerHTML = ''; // Clear previous content

        // Display each saved post
        posts.forEach(post => {
            addPostToDisplay(post.username, post.content);
        });
    }

    // Function to add a single post element to the display area
    function addPostToDisplay(username, content) {
        const postDiv = document.createElement('div');
        postDiv.classList.add('post');
        // Sanitize input lightly for basic display, consider more robust sanitization for production
        const safeUsername = encodeURIComponent(username);
        const safeContent = encodeURIComponent(content);
        postDiv.innerHTML = `
            <strong>${decodeURIComponent(safeUsername)}:</strong>
            <p>${decodeURIComponent(safeContent)}</p>
            <hr>
        `;
        displayArea.appendChild(postDiv);
    }

    // This is the function called by your HTML button's onclick="displayText()"
    window.displayText = function() {
        const usernameInput = document.getElementById('username');
        const contentInput = document.getElementById('postContent');
        const username = usernameInput.value;
        const content = contentInput.value;

        if (username.trim() === '' || content.trim() === '') {
            alert('Please enter both a username and content.');
            return;
        }

        // 2. Get existing posts, add the new one, and save back to localStorage
        const posts = JSON.parse(localStorage.getItem('forumPosts')) || [];
        const newPost = { username: username, content: content };
        posts.push(newPost);

        // Save the updated array back into localStorage
        localStorage.setItem('forumPosts', JSON.stringify(posts));

        // 3. Update the display without reloading the page
        addPostToDisplay(username, content);

        // Clear the input fields
        usernameInput.value = '';
        contentInput.value = '';
    };
});
