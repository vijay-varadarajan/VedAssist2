# VedAssist 2.0

by **Vijay Varadarajan**,
from VIT University, Vellore, India.

Video demo: 

Github Repo link: [VedAssist-Source](https://github.com/vijay-varadarajan/VedAssist2/)

<img src="readme_images\vedassist_home_design.png" alt="Home page image" width=420px height=200px>

## About this project

**VedAssist 2.0** is a Django web application designed to provide assistance for users seeking quick information on Ayurvedic medicines. 

This consists of a user-friendly web application that offers features such as a **symptom-based medicine recommendation system** and a **virtual Ayurvedic medicine store**.

## Inspiration

The inspiration behind "VedAssist 2.0" is **to make Ayurvedic medicine information accessible** to users who wish to explore and purchase these traditional remedies. 

The project aims to **bridge the gap between Ayurveda and modern technology** by providing a user-friendly interface for medicine recommendations and purchases.

## Features

### Predict Portal

<img src="readme_images\vedassist_predictor_design.png" alt="Home page image" width=420px height=200px>

- The "Predict" portal in "VedAssist 2.0" is designed to assist users in identifying Ayurvedic medicines based on the symptoms they are experiencing. It utilizes a symptom-based recommendation system to provide personalized suggestions for users.

- Each recommended medicine is accompanied by a detailed description, including its composition, recommended dosage, and potential side effects.

- Users can make an informed decision about which medicine is right for them based on this information.

### Shop Portal

<img src="readme_images\vedassist_shop_design.png" alt="Home page image" width=370px height=200px>

- The "Shop" portal in "VedAssist 2.0" is designed to assist users in purchasing Ayurvedic medicines. This portal provides a virtual store where users can browse and purchase Ayurvedic medicines.

- The portal displays a comprehensive list of available Ayurvedic medicines in a tabular format.

- Each medicine entry includes essential details such as the name, price, description, and an option to purchase.

### History page

<img src="readme_images\vedassist_history_design.png" alt="Home page image" width=420px height=300px>

- The "History" page in "VedAssist 2.0" displays a comprehensive list of all the transactions made by the user.

## Working / Usage instructions

- Visit the hosted URL ***www.vedassist.co***

- Scroll down on the **landing page** to read about the project and its features.

- Click on **Get Started** to register yourself or **Log in** if you already have an account.

- Or, you may use the **navbar** to go to the desired page.

<img src="readme_images\vedassist_navbar_design.png" alt="Home page image" width=420px height=40px>

- After logging in, you will be redirected to the **predict** page.

- Here, you can enter your symptoms and click on **Predict** to get a list of recommended medicines.

- This symptom and prediction data is **not stored anywhere**, in order to respect user privacy.

- You can click on **Shop** in the navbar to go to the shop page.

- There is a **searchbar** on the top of the page, where you can search for a specific medicine.

- Here, you can browse through the list of available medicines, read about them and click on **Buy** to purchase them.


- Your **account balance** is displayed on the top right corner of the page.

<img src="readme_images\vedassist_balance_design.png" alt="Home page image" width=160px height=40px>

- You can click on **+** to add money to your account.

- Balance will be updated respectively for each transaction.

- You can click on **History** in the navbar to go to the history page, where you will find the list of your transactions from the shop.

- Click on **Log out** in the navbar to log out of your account.


## Installation requirements

- To run this project yourself, you need to have **Python 3.6+** installed on your system.

- Clone this repository onto your github either by using the GUI or the following command:

```bash
git clone https://github.com/vijay-varadarajan/VedAssist2.git
```

- Install the required packages using the following command:

```bash
pip install -r requirements.txt
```

- Run the following command to start the server:

```bash
python manage.py runserver
```

- Open the following link in your browser to view the web application:

```bash
http://127.0.0.1:8000/
```

<details>
    <summary>
        <h2>References</h2>
    </summary>

+ [Python](https://docs.python.org/)
+ [Django](https://docs.djangoproject.com/)
+ [Bootstrap](https://getbootstrap.com/docs/4.0/getting-started/introduction/)
+ [Ayurvedic medicine](https://en.wikipedia.org/wiki/Ayurveda)

</details>
