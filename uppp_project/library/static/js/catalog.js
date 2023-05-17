function toggleDescription(id) {
    const description = document.getElementById(`description-${id}`);
    const button = document.getElementById(`btn-details-${id}`);
    if (description.style.display === "none") {
        description.style.display = "block";
    } else {
        description.style.display = "none";
    }
}

function reserveBook(id) {
    // Placeholder implementation
    console.log(`Книга ${id} забронирована!`);
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
    if (foundResults) {
        noResults.style.display = 'none';
    } else {
        noResults.style.display = 'block';
    }
}

function handleSearch(event) {
    if (event.keyCode === 13) {
        searchBooks();
        event.preventDefault();
    }
}