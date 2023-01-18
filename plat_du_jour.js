const webdriver = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const {Builder, By, Key, until} = require('selenium-webdriver');
const options = new chrome.Options();
options.addArguments('--headless');
options.addArguments('--disable-dev-shm-usage');
options.addArguments('--no-sandbox');
options.addArguments('--disable-setuid-sandbox');

async function getMenu() {
    let menu = [];
    let element = await driver.findElement(webdriver.By.xpath("//ul[@class='meal_foodies']"));
    let text = await element.getText();
    menu = text.split('\n');
    return menu;
}

let driver = new webdriver.Builder()
    .forBrowser('chrome')
    .setChromeOptions(options)
    .build();

let main_url = "https://www.crous-montpellier.fr/restaurant/resto-u-triolet-2/";

driver.get(main_url);

// driver.findElement(webdriver.By.xpath("//time[@class='menu_date_title']")).getText().then((text) => {
//    let date_du_menu = text.split();
//    // rest of the code
// });

// let date_du_jour = (new Date().toISOString().slice(0,10).split("-"))[2];

if(true){
    getMenu().then(menu => {

        let liste_menu = ["Entrée chaude", "Entrées froides", "Cuisine du monde", "Pastaria", "Saveurs de la mer 1", "Plat des régions", "Rôtisserie", "Saveurs de la mer 2", "Desserts"];
    
        let tous_menus = {};
        let menu_current = [];
    
        for (let plat of menu) {
            console.log(plat)
            if (liste_menu.includes(plat)) {
                if (menu_current.length>0) {
                    let keys = Object.keys(tous_menus);
                    tous_menus[keys[keys.length-1]] = menu_current;
                    menu_current=[];
                }
                tous_menus[plat]=[];
            } else {
                if (plat === "(plat végétarien)" || plat === "(plat unique)") {
                    menu_current[menu_current.length-1] = menu_current[menu_current.length-1]+" "+plat;
                } else {
                    menu_current.push(plat);
                }
            }
        }
        let keys = Object.keys(tous_menus);
        tous_menus[keys[keys.length-1]] = menu_current;
        menu_current=[];

    console.log(tous_menus);
    });
}