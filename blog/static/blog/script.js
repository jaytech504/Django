document.addEventListener('DOMContentLoaded', () => {
    const likeButton = document.getElementById('like-button');
    const likeCounter = document.getElementById('like-counter');

    let isLiked = false;
    let likeCount = 0;

    likeButton.addEventListener('click', () => {
        isLiked = !isLiked;
        likeCount = isLiked ? likeCount + 1 : likeCount - 1;

        likeCounter.textContent = likeCount;

        if (isLiked) {
            likeButton.classList.add('liked');
        } else {
            likeButton.classList.remove('liked');
        }

        likeButton.classList.add('clicked');
        setTimeout(() => {
            likeButton.classList.remove('clicked');
        }, 200);
    });
});