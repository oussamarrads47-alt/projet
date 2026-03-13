/**
 * TRANS-GEST — Forms JavaScript
 * Form validation and image preview utilities
 */
document.addEventListener('DOMContentLoaded', function () {

    // --- Image preview on file input ---
    document.querySelectorAll('input[type="file"][accept*="image"]').forEach(function (input) {
        input.addEventListener('change', function () {
            var file = this.files[0];
            if (!file) return;

            // Validate file size (max 5 MB)
            if (file.size > 5 * 1024 * 1024) {
                alert('La taille du fichier ne doit pas dépasser 5 Mo.');
                this.value = '';
                return;
            }

            // Validate file type
            if (!file.type.startsWith('image/')) {
                alert('Veuillez sélectionner un fichier image valide.');
                this.value = '';
                return;
            }

            // Show preview
            var existingPreview = this.parentElement.querySelector('.image-preview');
            if (existingPreview) existingPreview.remove();

            var reader = new FileReader();
            var parent = this.parentElement;
            reader.onload = function (e) {
                var preview = document.createElement('div');
                preview.className = 'image-preview';
                preview.style.cssText = 'margin-top:12px;';
                preview.innerHTML = '<img src="' + e.target.result + '" style="max-width:200px;max-height:200px;border-radius:12px;border:2px solid rgba(59,130,246,0.3);object-fit:cover;" />';
                parent.appendChild(preview);
            };
            reader.readAsDataURL(file);
        });
    });

    // --- Form validation visual feedback ---
    document.querySelectorAll('.form-control').forEach(function (input) {
        input.addEventListener('blur', function () {
            if (this.hasAttribute('required') && !this.value.trim()) {
                this.style.borderColor = '#EF4444';
            } else if (this.value.trim()) {
                this.style.borderColor = '#10B981';
                setTimeout(function () {
                    input.style.borderColor = '';
                }, 1500);
            }
        });

        input.addEventListener('focus', function () {
            this.style.borderColor = '';
        });
    });

    // --- Number inputs: prevent negative values ---
    document.querySelectorAll('input[type="number"]').forEach(function (input) {
        input.addEventListener('input', function () {
            var min = parseInt(this.getAttribute('min') || '0');
            if (parseInt(this.value) < min) {
                this.value = min;
            }
        });
    });

    // --- Date validation: return date cannot be before sortie date ---
    var dateSortie = document.querySelector('[name="date_sortie"]');
    var dateRetour = document.querySelector('[name="date_retour"]');
    if (dateSortie && dateRetour) {
        dateRetour.addEventListener('change', function () {
            if (dateSortie.value && this.value) {
                if (new Date(this.value) < new Date(dateSortie.value)) {
                    alert('La date de retour ne peut pas être antérieure à la date de sortie.');
                    this.value = '';
                }
            }
        });
    }
});
