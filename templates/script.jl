const pages = [
    "Page 1 Content",
    "Page 2 Content",
    "Page 3 Content"
    // Add more pages as needed
];

let currentPageIndex = 0;
const contentElement = document.getElementById('content');

function showPage(pageIndex) {
    contentElement.textContent = pages[pageIndex];
}

function prevPage() {
    if (currentPageIndex > 0) {
        currentPageIndex--;
        showPage(currentPageIndex);
    }
}

function nextPage() {
    if (currentPageIndex < pages.length - 1) {
        currentPageIndex++;
        showPage(currentPageIndex);
    }
}

