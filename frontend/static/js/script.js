document.addEventListener('DOMContentLoaded', () => {
    const countrySelect = document.getElementById('country');
    const signupForm = document.getElementById('signupForm');
    const signupButton = document.querySelector('.signup-button');

    const loadingText = 'Signing up...';
    const defaultText = 'Sign Up';

    async function fetchCountries() {
        try {
            const response = await fetch('https://restcountries.com/v3.1/all?fields=name,currencies');
            if (!response.ok) {
                throw new Error('Failed to fetch countries');
            }
            const countries = await response.json();
            
            countries.sort((a, b) => a.name.common.localeCompare(b.name.common));

            countries.forEach(country => {
                const option = document.createElement('option');
                option.value = country.name.common;
                option.textContent = country.name.common;
                countrySelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error fetching countries:', error);
            const option = document.createElement('option');
            option.textContent = 'Failed to load countries';
            option.disabled = true;
            countrySelect.appendChild(option);
        }
    }

    fetchCountries();

    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        if (password !== confirmPassword) {
            alert("Passwords do not match. Please try again.");
            return;
        }

        // Disable button and show loading state
        signupButton.disabled = true;
        signupButton.textContent = loadingText;

        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            password: password,
            country: countrySelect.value
        };

        try {
            // Simulate an API call
            await new Promise(resolve => setTimeout(resolve, 2000));
            console.log('Form data submitted:', formData);
            alert('Signup successful! You can now log in.');
            signupForm.reset();
        } catch (error) {
            console.error('Signup failed:', error);
            alert('An error occurred during signup. Please try again.');
        } finally {
            // Re-enable button and reset text
            signupButton.disabled = false;
            signupButton.textContent = defaultText;
        }
    });
});
