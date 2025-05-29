document.addEventListener('DOMContentLoaded', function() {

    const flightTypeSelect = document.getElementById('id_flight_type');

    const speed = document.querySelector('.form-row.field-speed')
    const cameraViewRow = document.querySelector('.form-row.field-camera_view_direction')
    const cameraPitch = document.querySelector('.form-row.field-camera_pitch')

    const position = document.querySelector('[aria-labelledby="fieldset-0-1-heading"]')
    const rotation = document.querySelector('[aria-labelledby="fieldset-0-2-heading"]')

    const inlineSection = document.getElementById('flight_points-group');


    function showEl(el) {
        el.style.display = ''
    }

    function hideEl(el) {
        el.style.display = 'none'
    }

    function toggleFields() {
        const val = flightTypeSelect.value;

        hideEl(speed)
        hideEl(cameraViewRow)
        hideEl(cameraPitch)
        hideEl(position)
        hideEl(rotation)
        hideEl(inlineSection)

        if (val === 'static_frame') {
            showEl(position)
            showEl(rotation)
        }
        if (val === 'points_flight') {
            showEl(speed)
            showEl(cameraViewRow)
            showEl(cameraPitch)
            showEl(inlineSection)
        }
        if (val === 'panorama') {
            showEl(speed)
            showEl(cameraPitch)
            showEl(position)
        }
    }

    toggleFields();
    flightTypeSelect.addEventListener('change', toggleFields);
});
