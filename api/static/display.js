function whenReady(selector, callback) {
    const el = document.querySelector(selector);
    if (el) {
        callback(el);
    } else {
        setTimeout(() => whenReady(selector, callback), 10);
    }
}

whenReady('#select2-id_camera_view_direction-container', () => {
    const flightTypeSelect = document.querySelector('#select2-id_flight_type-container');

    const speed = document.querySelector('div.form-group.field-speed')
    const cameraViewRow = document.querySelector('div.form-group.field-camera_view_direction')
    const cameraPitch = document.querySelector('div.form-group.field-camera_pitch')

    const position = document.querySelector('#jazzy-tabs > li:nth-child(2)')
    const rotation = document.querySelector('#jazzy-tabs > li:nth-child(3)')

    const inlineSection = document.querySelector('#jazzy-tabs > li:nth-child(4)');


    function showEl(el) {
        el.style.display = ''
    }

    function hideEl(el) {
        el.style.display = 'none'
    }

    function toggleFields() {
        const val = flightTypeSelect.title;

        hideEl(speed)
        hideEl(cameraViewRow)
        hideEl(cameraPitch)
        hideEl(position)
        hideEl(rotation)
        hideEl(inlineSection)

        if (val === 'Статичний кадр') {
            showEl(position)
            showEl(rotation)
        }
        if (val === 'Обліт по точках') {
            showEl(speed)
            showEl(cameraViewRow)
            showEl(cameraPitch)
            showEl(inlineSection)
        }
        if (val === 'Панорама навколо') {
            showEl(speed)
            showEl(cameraPitch)
            showEl(position)
        }
    }

    toggleFields();
    const observer = new MutationObserver(toggleFields);

    observer.observe(flightTypeSelect, { childList: true, characterData: true, subtree: true });
});
