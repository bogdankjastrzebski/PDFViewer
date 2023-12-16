let currentPageIndex = 0;

const configPromise = fetch('/info')
    .then(response => response.json());


const pagesPromises = 


function showPage(pageIndex) {
    
    fetch(`/content/${pageIndex}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
            } else {
                const img = document.getElementById("pdfImageContainer");
                img.innerHTML = `<img src="data:image/png;base64,${data.content}" alt="PDF Page Image">`;
            }
        })
        .catch(error => console.error('Error fetching content:', error));
}


function prevPage() {
    configPromise.then(config => {
        if (currentPageIndex > 0) {
            currentPageIndex--;
            showPage(currentPageIndex);
        }
    })
}


function nextPage() {
    configPromise.then(config => {
        if (currentPageIndex < config.pageCount) {
            currentPageIndex++;
            showPage(currentPageIndex);
        }
    })
}


document.addEventListener('DOMContentLoaded', function () {
    showPage(0);  // Fetch and display PDF image for page 1
});


document.addEventListener('keydown', function (event) {
    switch (event.key) {
        case 'ArrowLeft':
            console.log('Left arrow key pressed');
            prevPage()
            break;
        case 'ArrowRight':
            console.log('Right arrow key pressed');
            nextPage()
            break;
        case 'h':
            console.log('h key pressed');
            prevPage()
            break;
        case 'l':
            console.log('l key pressed');
            nextPage()
            break;
        default:
            break;
    }
});


// Handle browser back/forward navigation
// window.onpopstate = function(event) {
//    const path = window.location.pathname;
//    const pageIndex = parseInt(path.slice(-1)) || 0;
//    
//    if (!isNaN(pageIndex)) {
//        showPage(pageIndex);
//    }
//};
