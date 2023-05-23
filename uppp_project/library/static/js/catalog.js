function toggleDescription(id) {
    const overlay = document.getElementById(`book-overlay-${id}`);
    const description = document.getElementById(`description-${id}`);
    const isHidden = overlay.style.display === 'none';

    if (isHidden) {
        overlay.style.display = 'block';
    } else {
        overlay.style.display = 'none';
    }
}

function reserveBook(id) {
    // Placeholder implementation
    console.log(`Книга ${id} забронирована!`);
}

function showAllBooks() {
    const bookContainers = document.getElementsByClassName('book-container');

    for (let i = 0; i < bookContainers.length; i++) {
        const bookContainer = bookContainers[i];
        bookContainer.style.display = 'block';
    }
}

function showBooksByGenre(genre) {
    const bookContainers = document.getElementsByClassName('book-container');

    for (let i = 0; i < bookContainers.length; i++) {
        const bookContainer = bookContainers[i];
        const bookGenre = bookContainer.querySelector('.book-genre').textContent;

        if (bookGenre === genre) {
            bookContainer.style.display = 'block';
        } else {
            bookContainer.style.display = 'none';
        }
    }
}

function searchBooks() {
    const searchInput = document.getElementById('search-input').value.toLowerCase();
    const bookContainers = document.getElementsByClassName('book-container');
    let foundResults = false;

    for (let i = 0; i < bookContainers.length; i++) {
        const bookTitle = bookContainers[i].getElementsByClassName('book-title')[0].textContent.toLowerCase();
        const bookAuthor = bookContainers[i].getElementsByClassName('book-author')[0].textContent.toLowerCase();

        if (bookTitle.includes(searchInput) || bookAuthor.includes(searchInput)) {
            bookContainers[i].style.display = 'block';
            foundResults = true;
        } else {
            bookContainers[i].style.display = 'none';
        }
    }

    const noResults = document.getElementById('no-results');
    const genresContainer = document.getElementById('genres-container');

    if (foundResults) {
        noResults.style.display = 'none';
        genresContainer.style.display = 'block';
    } else {
        noResults.style.display = 'block';
        genresContainer.style.display = 'none';
    }
}

function handleSearch(event) {
    if (event.keyCode === 13) {
        searchBooks();
        event.preventDefault();
    }
}