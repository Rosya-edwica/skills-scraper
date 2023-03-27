package headhunter

import (
	"fmt"
	"github.com/Rosya-edwica/skills-scraper/src/logger"
	"github.com/Rosya-edwica/skills-scraper/src/models"
	"github.com/tidwall/gjson"
)

func GetVacanciesByQuery(city models.City, professionName string, professionId int) {
	url := CreateLink(professionName, city.HH_ID)
	checkCaptcha(url)
	json, err := GetJson(url)
	if err != nil {
		logger.Log.Printf("Ошибка при подключении к странице с вакансиями: %s. Error: %s", err, url)
		return
	}
	pagesCount := gjson.Get(json, "pages").Int()
	found := gjson.Get(json, "found").Int()
	logger.Log.Printf("Профессия: %s | Город: %s | Найдено: %d", professionName, city.Name, found)
	for page := 0; page < int(pagesCount); page++ {
		ParseVacanciesFromPage(fmt.Sprintf("%s&page=%d", url, page), city.EDWICA_ID, professionId)
	}
	return
}

func ParseVacanciesFromPage(url string, city_edwica int, id_profession int) {
	json, err := GetJson(url)
	if err != nil {
		logger.Log.Printf("Не удалось подключиться к странице %s.\nТекст ошибки: %s", err, url)
		return
	}

	items := gjson.Get(json, "items").Array()
	for _, item := range items {
		scrapeVacancy(item.Get("url").String(), city_edwica, id_profession)
	}
	return
}
