// it remove cache data when referece page it will not send data automatic
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}
// button click goto home page
function homePage() {
    window.location.href = '{% url "welcomepage" %}';
}