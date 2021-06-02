function getFavorite() {
    return JSON.parse(localStorage.getItem('favorite')) || [];
}

function pushFavorite(image_id) {
    let favorite = getFavorite();
    if (favorite.indexOf(image_id) == -1) {
        favorite.push(image_id);
    }
    localStorage.setItem('favorite', JSON.stringify(favorite));
}

function popFavorite(image_id) {
    let favorite = getFavorite();
    if (favorite.indexOf(image_id) != -1) {
        favorite.splice(favorite.indexOf(image_id), 1);
    }
    localStorage.setItem('favorite', JSON.stringify(favorite));
}

class ImageModel {
    constructor(data) {
        this.id = ko.observable(data.id);
        this.like = ko.observable(data.like);
        this.tag = ko.observableArray(data.tag);
    }

    toggle(data, node) {
        console.log(arguments);
        if (this.like()) {
            popFavorite(this.id());
            this.like(false);
        } else {
            pushFavorite(this.id());
            this.like(true);
        }
        animateCSS(node.children[0], 'heartBeat');
    }
}