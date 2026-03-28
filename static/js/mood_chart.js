document.addEventListener("DOMContentLoaded", function () {

const ctx = document.getElementById("moodChart");

if (ctx) {

    new Chart(ctx, {
        type: "pie",
        data: {
            labels: [
                "Happy 😊",
                "Sad 😔",
                "Angry 😡",
                "Excited 🤩",
                "Neutral 😐"
            ],
            datasets: [{
                data: moodData,
                backgroundColor: [
                    "#4CAF50",
                    "#2196F3",
                    "#F44336",
                    "#FF9800",
                    "#9E9E9E"
                ]
            }]
        }
    });

}

});