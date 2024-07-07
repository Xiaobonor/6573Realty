// app/static/tag_user/script.js
let questions = [];
let answers = {};
let currentQuestion = null;

$(document).ready(function() {
    displayInitialQuestions();
});

$('#sendButton').click(async function() {
    await handleUserInput();
});

$('#userInput').keydown(async function(event) {
    if (event.key === 'Enter') {
        await handleUserInput();
    }
});

$('#closePopup').click(function() {
    $('#propertyPopup').hide();
    $('#container').css('filter', 'none');
});

$('#refreshButton').click(async function() {
    await refreshProperties();
});

$('#submitSelectionButton').click(async function() {
    await submitSelectedProperties();
});

function disableInput() {
    $('#userInput').attr('disabled', true);
    $('#sendButton').attr('disabled', true);
}

function enableInput() {
    $('#userInput').attr('disabled', false);
    $('#sendButton').attr('disabled', false);
}

async function handleUserInput() {
    const userInput = $('#userInput').val();
    if (!userInput) return;

    appendMessage(userInput, 'user');
    $('#userInput').val('');
    disableInput();

    if (currentQuestion) {
        answers[currentQuestion.question] = userInput;
        if (questions.length === 0) {
            await submitAnswers();
        } else {
            displayNextQuestion();
            enableInput();
        }
    } else {
        displayInitialQuestions();
    }
}

function displayInitialQuestions() {
    questions = [
        { question: '請輸入您接受的最高租金價格：' },
        { question: '請輸入您的租屋預計位置：' },
        {
            question: '請選擇您想找的房子類型：',
            options: ['entire_home', 'studio', 'shared_room']
        },
        {
            question: '請選擇房屋格局：',
            options: ['1_room', '2_rooms', '3_rooms', '4_rooms']
        },
        {
            question: '請選擇建築類型：',
            options: ['apartment', 'elevator_building', 'townhouse', 'villa', 'N/A']
        }
    ];

    displayNextQuestion();
}

async function submitAnswers() {
    disableInput();

    $.ajax({
        url: '/rental/submit_answers',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ answers: answers }),
        success: function(data) {
            if (data.success) {
                displayRentalProperties(data.properties);
            } else {
                enableInput();
                showError({ title: '錯誤', message: data.error || '無法提交您的回答' });
            }
        },
        error: function() {
            enableInput();
            showError({ title: '錯誤', message: '無法提交您的回答' });
        }
    });
}

function displayNextQuestion() {
    if (!questions || questions.length === 0) {
        console.error('No more questions to display');
        return;
    }

    currentQuestion = questions.shift();
    const questionDiv = $('<div>').addClass('system').text(currentQuestion.question);

    if (currentQuestion.options && currentQuestion.options.length > 0) {
        currentQuestion.options.forEach(option => {
            const optionDiv = $('<div>').addClass('option-card').text(option).click(async () => {
                answers[currentQuestion.question] = option;
                appendMessage(option, 'user');
                disablePreviousOptions();
                if (questions.length === 0) {
                    await submitAnswers();
                } else {
                    displayNextQuestion();
                    enableInput();
                }
            });
            questionDiv.append(optionDiv);
        });
    } else {
        questionDiv.append($('<div>').addClass('option-card').text('請輸入您的回答'));
    }

    $('#chatBox').append(questionDiv).scrollTop($('#chatBox')[0].scrollHeight);
}

function disablePreviousOptions() {
    $('.option-card').css({ 'pointer-events': 'none', 'opacity': '0.5' });
}

function appendMessage(message, sender) {
    const messageDiv = $('<div>').addClass(sender).text(message);
    $('#chatBox').append(messageDiv).scrollTop($('#chatBox')[0].scrollHeight);
}

function displayRentalProperties(properties) {
    $('#container').css('filter', 'blur(5px)');
    $('#propertyPopup').show();

    const propertyContainer = $('#propertyContainer');
    propertyContainer.empty();

    properties.forEach(property => {
        const propertyCard = $(`
            <div class="property-card" data-uuid="${property.uuid}">
                <div class="image-container">
                    <img src="${property.images[0]}" alt="${property.name}">
                    <button class="prev-image"><i class="fas fa-chevron-left"></i></button>
                    <button class="next-image"><i class="fas fa-chevron-right"></i></button>
                </div>
                <h2>${property.name}</h2>
                <p>${property.description}</p>
            </div>
        `);

        propertyCard.click(function() {
            $(this).toggleClass('selected');
        });

        propertyCard.find('.prev-image').click(function(event) {
            event.stopPropagation();
            showPrevImage(propertyCard, property.images);
        });

        propertyCard.find('.next-image').click(function(event) {
            event.stopPropagation();
            showNextImage(propertyCard, property.images);
        });

        propertyContainer.append(propertyCard);
    });
}

function showPrevImage(propertyCard, images) {
    const img = propertyCard.find('img');
    const currentIndex = images.indexOf(img.attr('src'));
    const newIndex = (currentIndex - 1 + images.length) % images.length;
    img.attr('src', images[newIndex]);
}

function showNextImage(propertyCard, images) {
    const img = propertyCard.find('img');
    const currentIndex = images.indexOf(img.attr('src'));
    const newIndex = (currentIndex + 1) % images.length;
    img.attr('src', images[newIndex]);
}

async function refreshProperties() {
    disableInput();

    $.ajax({
        url: '/rental/refresh_properties',
        method: 'GET',
        success: function(data) {
            if (data.success) {
                displayRentalProperties(data.properties);
            } else {
                showError({ title: '錯誤', message: data.error || '無法獲取物件' });
            }
        },
        error: function() {
            showError({ title: '錯誤', message: '無法獲取物件' });
        }
    }).always(function() {
        enableInput();
    });
}

async function submitSelectedProperties() {
    const selectedProperties = $('.property-card.selected').map(function() {
        return $(this).data('uuid');
    }).get();

    disableInput();

    $.ajax({
        url: '/rental/submit_selected_properties',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ selected_properties: selectedProperties }),
        success: function(data) {
            if (data.success) {
                window.location.href = '/';
            } else {
                showError({ title: '錯誤', message: data.error || '無法提交您的選擇' });
            }
        },
        error: function() {
            showError({ title: '錯誤', message: '無法提交您的選擇' });
        }
    }).always(function() {
        enableInput();
    });
}

function showError(error) {
    alert(`${error.title}: ${error.message}`);
}

function showNotification(message, duration) {
    const notificationDiv = $('<div>').addClass('notification').text(message);
    $('body').append(notificationDiv);
    setTimeout(() => {
        notificationDiv.remove();
    }, duration);
}
