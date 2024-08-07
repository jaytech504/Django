document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.fa-heart').forEach(function(button) {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            fetch("{% url 'like_post' %}", {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ post_id: postId })
            })
            .then(response => response.json())
            .then(data => {
                const likeButton = this;
                if (data.liked) {
                    likeButton.classList.remove('far');
                    likeButton.classList.add('fas');
                } else {
                    likeButton.classList.remove('fas');
                    likeButton.classList.add('far');
                }
                likeButton.nextElementSibling.textContent = `${data.likes_count} likes`;
            },bind(this));
        });
    });
});