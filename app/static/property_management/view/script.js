let currentImageIndex = 0;

// 定義映射字典
const propertyTypeDict = {
    "studio": "獨立套房",
    "entire_home": "整層住家",
    "shared_room": "雅房"
};

const layoutDict = {
    "1_room": "一室",
    "2_rooms": "兩室",
    "3_rooms": "三室",
    "4_rooms": "四室"
};

const buildingTypeDict = {
    "elevator_building": "電梯大樓",
    "apartment": "公寓",
    "townhouse": "透天厝",
    "villa": "別墅"
};

document.getElementById('property-name').innerText = propertyData.name;
document.getElementById('detailed-description').innerText = propertyData.detailed_description;
document.getElementById('landlord').innerText = propertyData.landlord;
document.getElementById('address').innerText = propertyData.address;
document.getElementById('floor-info').innerText = propertyData.floor_info;
document.getElementById('rent-price').innerText = propertyData.rent_price + ' 元/月';
document.getElementById('deposit').innerText = propertyData.deposit + ' 元';
document.getElementById('property-type').innerText = propertyTypeDict[propertyData.property_type];
document.getElementById('layout').innerText = layoutDict[propertyData.layout];
document.getElementById('building-type').innerText = buildingTypeDict[propertyData.building_type];
document.getElementById('area').innerText = propertyData.area + ' 坪';
document.getElementById('decoration-style').innerText = propertyData.decoration_style;
document.getElementById('min-lease-months').innerText = propertyData.min_lease_months + ' 個月';
document.getElementById('has-balcony').innerText = propertyData.has_balcony ? '是' : '否';
document.getElementById('view-count').innerText = propertyData.view_count + ' 次';
document.getElementById('created-at').innerText = new Date(propertyData.created_at).toLocaleString('zh-TW');
document.getElementById('last-updated-at').innerText = new Date(propertyData.last_updated_at).toLocaleString('zh-TW');

const imageGallery = document.getElementById('image-gallery');
const dots = document.getElementById('dots');
propertyData.images.forEach((base64Image, index) => {
    const img = document.createElement('img');
    img.src = base64Image;
    img.style.display = index === 0 ? 'block' : 'none';
    imageGallery.appendChild(img);

    const dot = document.createElement('span');
    dot.className = index === 0 ? 'active' : '';
    dot.onclick = () => showImage(index);
    dots.appendChild(dot);
});

function showImage(index) {
    const images = imageGallery.querySelectorAll('img');
    const dotElements = dots.querySelectorAll('span');
    images[currentImageIndex].style.display = 'none';
    dotElements[currentImageIndex].classList.remove('active');
    images[index].style.display = 'block';
    dotElements[index].classList.add('active');
    currentImageIndex = index;
}

function prevImage() {
    const newIndex = (currentImageIndex - 1 + propertyData.images.length) % propertyData.images.length;
    showImage(newIndex);
}

function nextImage() {
    const newIndex = (currentImageIndex + 1) % propertyData.images.length;
    showImage(newIndex);
}

function updateIconAvailability(items, itemType) {
    items.forEach(item => {
        document.getElementById(item).style.color = '#000';
    });

    const allItems = {
        furniture: ['sofa', 'bed', 'desk_chair', 'dining_table', 'wardrobe', 'bookshelf', 'tv_stand', 'nightstand', 'dresser', 'shoe_rack'],
        amenities: ['wifi', 'washing_machine', 'refrigerator', 'water_heater', 'microwave', 'air_conditioner', 'heater', 'tv', 'dishwasher', 'oven', 'fan', 'air_purifier', 'fire_extinguisher', 'smoke_detector', 'electric_stove']
    };

    allItems[itemType].forEach(item => {
        if (!items.includes(item)) {
            document.getElementById(item).style.color = '#ccc';
        }
    });
}

document.getElementById('landlord').innerText = propertyData.landlord_info;

function contactLandlord() {
    const landlordLine = propertyData.landlord_line;
    window.open(`https://line.me/R/ti/p/${landlordLine}`, '_blank');
}

updateIconAvailability(propertyData.furniture, 'furniture');
updateIconAvailability(propertyData.amenities, 'amenities');
