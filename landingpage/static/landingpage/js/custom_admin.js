document.addEventListener('DOMContentLoaded', function () {
    // Wait for TinyMCE to be initialized
    tinymce.init({
        selector: '#id_content', // The selector for the TinyMCE editor
        setup: function (editor) {
            editor.on('init', function () {
                // Insert content directly as HTML when TinyMCE is initialized
                editor.setContent('<h2>Hello World</h2><p>This is a <strong>sample</strong> content.</p>');
            });
        },
        // Ensure content is not sanitized (allow full HTML)
        valid_elements: '*[*]', // Allow all elements and attributes (use caution)
        paste_as_text: true, // Ensure pasted content stays as raw HTML
        height: 300,
        menubar: false,
        toolbar: 'bold italic underline | alignleft aligncenter alignright',
    });

    // To handle dynamic changes and ensure the preview always reflects HTML tags
    const contentField = document.querySelector('#id_content');
    contentField.addEventListener('input', function () {
        const previewIframe = document.querySelector('.tox-editor-container iframe'); // Get TinyMCE iframe
        const previewDocument = previewIframe.contentDocument || previewIframe.contentWindow.document; // Get the iframe's document

        // Set the iframe content as the HTML content of the editor
        previewDocument.body.innerHTML = contentField.value;
    });
});
