package headhunter

import (
	"fmt"
	"github.com/tidwall/gjson"
	"strings"

	"github.com/Rosya-edwica/skills-scraper/src/logger"
	"github.com/Rosya-edwica/skills-scraper/src/models"
	"github.com/Rosya-edwica/skills-scraper/src/mysql"
)

func scrapeVacancy(url string, city_edwica int, id_profession int) {
	var vacancy models.VacancySkills
	checkCaptcha(url)
	json, err := GetJson(url)
	if err != nil {
		logger.Log.Printf("Ошибка при подключении к странице %s.\nТекст ошибки: %s", err, url)
		return
	}

	vacancy.CityId = city_edwica
	vacancy.ProfessionId = id_profession
	vacancy.Skills = getSkills(json)
	vacancy.Title = gjson.Get(json, "name").String()
	vacancy.Url = gjson.Get(json, "alternate_url").String()
	mysql.SaveOneVacancy(vacancy)
}

func getSkills(vacancyJson string) string {
	var skills []string
	for _, item := range gjson.Get(vacancyJson, "key_skills").Array() {
		skills = append(skills, item.Get("name").String())
	}
	languages := getLanguages(vacancyJson)
	skills = append(skills, languages...)
	return strings.Join(skills, "|")
}

func getLanguages(vacancyJson string) (languages []string) {
	for _, item := range gjson.Get(vacancyJson, "languages").Array() {
		lang := item.Get("name").String()
		level := item.Get("level.name").String()
		languages = append(languages, fmt.Sprintf("%s (%s)", lang, level))
	}
	return
}