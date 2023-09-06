(() => {
    'use strict'
    const highlightCategories = function(categoriesElem) {
        categoriesElem.querySelectorAll('a').forEach(element => {
            element.classList.remove('active');
        });
        const mostVisibleElem = mostVisible('.waggylabs-post-list-item');
        if (mostVisibleElem) {
            const postCategoriesElem = mostVisibleElem.querySelector('.waggylabs-post-categories');
            postCategoriesElem.querySelectorAll('span').forEach(element => {
                let catElem = categoriesElem.querySelector('a[data-slug="' + element.getAttribute('data-slug') + '"]');
                catElem.classList.add('active');
            });
        }
    }

    const highlightTags = function(tagsElem) {
        tagsElem.querySelectorAll('a').forEach(element => {
            element.classList.remove('active');
        });
        const mostVisibleElem = mostVisible('.waggylabs-post-list-item');
        if (mostVisibleElem) {
            const postTagsElem = mostVisibleElem.querySelector('.waggylabs-post-tags');
            postTagsElem.querySelectorAll('span').forEach(element => {
                let tagElem = tagsElem.querySelector('a[data-slug="' + element.getAttribute('data-slug') + '"]');
                tagElem.classList.add('active');
            });
        }
    }

    window.addEventListener('DOMContentLoaded', function() {
        const categoriesElem = document.querySelector('.waggylabs-post-category-list');
        const tagsElem = document.querySelector('.waggylabs-post-tag-list');
        const postElems = document.querySelectorAll('.waggylabs-post-list-item');
        if (categoriesElem && postElems) {
            highlightCategories(categoriesElem);
            window.addEventListener('scroll', function() {
                highlightCategories(categoriesElem);
            });
        }
        if (tagsElem && postElems) {
            highlightTags(tagsElem);
            window.addEventListener('scroll', function() {
                highlightTags(tagsElem);
            });
        }
    });
})()