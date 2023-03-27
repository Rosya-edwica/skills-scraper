package headhunter

import (
	"errors"
	"github.com/Rosya-edwica/skills-scraper/src/logger"
	"github.com/Rosya-edwica/skills-scraper/src/models"
	"github.com/Rosya-edwica/skills-scraper/src/mysql"

	"sync"
)

const GroupSize = 10

func Go() {
	professions := mysql.GetProfessions()
	if len(professions) == 0 {
		checkErr(errors.New("Пустой список профессий. Нечего искать"))
	}
	for _, profession := range professions {
		parseProfession(profession)
	}

}

func parseProfession(profession models.Profession) {
	logger.Log.Printf("Ищем профессию `%s`", profession.Title)
	groups := groupCities()
	for _, group := range groups {
		var wg sync.WaitGroup
		wg.Add(len(group))
		for _, city := range group {
			go parseProfessionInCity(city, profession, &wg)
		}
		wg.Wait()
	}
	mysql.SetParsedStatusToProfession(profession.Id)
	logger.Log.Printf("Профессия %s спарсена", profession.Title)

}

func groupCities() (groups [][]models.City) {
	cities := mysql.GetCities()
	citiesCount := len(cities)
	var limit int
	for i := 0; i < citiesCount; i += GroupSize {
		limit += GroupSize
		if limit > citiesCount {
			limit = citiesCount
		}
		group := cities[i:limit]
		groups = append(groups, group)
	}
	logger.Log.Printf("Ведем поиск профессии в  %d городах одновременно", GroupSize)
	return
}

func parseProfessionInCity(city models.City, profession models.Profession, wg *sync.WaitGroup) {
	defer wg.Done()
	GetVacanciesByQuery(city, profession.Title, profession.Id)
}
