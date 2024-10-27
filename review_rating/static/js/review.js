
function showModal() {
    const modal = document.getElementById("crudModal");
    const modalContent = document.getElementById("crudModalContent");
  
    modal.classList.remove("hidden");
    setTimeout(() => {
      modalContent.classList.remove("opacity-0", "scale-95");
      modalContent.classList.add("opacity-100", "scale-100");
    }, 50);
  }
  
function hideModal() {
    const modal = document.getElementById("crudModal");
    const modalContent = document.getElementById("crudModalContent");

    modalContent.classList.remove("opacity-100", "scale-100");
    modalContent.classList.add("opacity-0", "scale-95");

    setTimeout(() => {
        modal.classList.add("hidden");
    }, 150);
}

const stars = document.querySelectorAll('input[name="rating"]');

stars.forEach(star => {
    star.addEventListener('change', () => {
        stars.forEach(s => {
            const label = document.querySelector(`label[for="${s.id}"]`);
            label.classList.remove('text-yellow-500');
            label.classList.add('text-gray-400');
        });
        
        for (let i = 0; i < star.value; i++) {
            const label = document.querySelector(`label[for="star${i + 1}"]`);
            label.classList.remove('text-gray-400');
            label.classList.add('text-yellow-500');
        }
    });
});

async function refreshReviews() {
    document.getElementById("review_cards").innerHTML = "";
    document.getElementById("review_cards").className = "";
    const reviews = await getReviews();
    let htmlString = "";
    let classNameString = "";

    if (reviews.length === 0) {
        classNameString = "flex flex-col items-center justify-center min-h-[24rem] p-6";
        htmlString = `
            <div class="flex flex-col items-center justify-center min-h-[24rem] p-6">
                <p class="text-center text-gray-600 mt-4">Belum ada yang mereview seller.</p>
            </div>
        `;
    }
    else {
        classNameString = "columns-1 sm:columns-2 lg:columns-3 gap-6 space-y-6 w-full"
        reviews.forEach((item) => {
            const rating = item.rating;
            const filledStars = '<img src="{% static \'image/star_fill.svg\' %}" class="w-6 h-6">';
            const emptyStars = '<img src="{% static \'image/star_border.svg\' %}" class="w-6 h-6">';
            const starsHtml = 
                filledStars.repeat(rating) + 
                emptyStars.repeat(5 - rating);
            htmlString += `
                <div class="w-full bg-white shadow-md rounded-3xl p-6 max-h-64 overflow-hidden">
                <div class="w-full flex justify-between items-center">
                    <div class="w-fit space-x-2 flex items-center">
                        <img src="${item.reviewer.user_profile.profile_picture}" class="w-8 h-8 rounded-full">
                        <p class="albert-sans-semibold">${item.reviewer.user_profile.user.username}</p>
                    </div>
                    <div class="w-fit space-x-1 flex">
                        ${starsHtml}
                    </div>
                </div>
                <div class="mt-4 max-h-full overflow-hidden">
                    <p class="overflow-hidden text-ellipsis" style="font-family:'Albert Sans', sans-serif; display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical;">
                        ${item.review}
                    </p>
                </div>
            </div>
            `;
        });
    }
    document.getElementById("review_cards").className = classNameString;
    document.getElementById("review_cards").innerHTML = htmlString;
}


async function addReview() {
    try {
        const formData = new FormData(document.querySelector("#reviewForm"));
        formData.append("reviewee_username", sellerUsername); 

        const response = await fetch(`/profile/${sellerUsername}/add_review/`, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Failed to add entry");
        }

        document.getElementById("reviewForm").reset();
        hideModal();
        refreshReviews();
    } catch (error) {
        console.error("Error creating forum entry:", error);
    }
}


document.getElementById("cancelButton").addEventListener("click", hideModal);
document.getElementById("closeModalBtn").addEventListener("click", hideModal);
document.getElementById("reviewForm").addEventListener("submit", (e) => {
    e.preventDefault();
    addReview();
  })