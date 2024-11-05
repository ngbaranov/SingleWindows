import enum


class Departments(enum.Enum):
    Management = "Руководство"
    Administrative = "Административный отдел"
    Accounting = "Бухгалтерия"
    Metrology = "Бюро метрологии"
    Passes = "Бюро пропусков"
    Dispatcher = "Диспетчерская служба"
    Medical = "Здравпункт"
    Commercial = "Коммерческий отдел"
    Moscow = "Московское отделение"
    Mehanical = "Отдел главного механика"
    Power = "Отдел главного энергетика"
    IT = "Отдел информационных технологий"
    HR = "Отдел кадров"
    Logistics = "Отдел логистики"
    Safety = "Охрана труда"
    OTK = "ОТК"
    Builders = "Отдел эксплуатации зданий и сооружений"
    Secrecy = "1 отдел"
    Technical = "Производственно-технический отдел"
    Repair = "Ремонтно-строительный участок"
    Composition = "Складское хозяйство"
    Security = "СБиР"
    Quality = "Служба качества"
    Financial = "Финансовый отдел"
    Legal = "Юридический отдел"
    Trade = "Профсоюзный комитет"
    Cafe = "Столовая"
    Transport = "Транспортная служба"
    Powersuple = "Участок электроснабжения"
    Workshop = "ЦАП"
    Firstsection = "Участок №1"
    Preciousmetals = "Участок по аффинажу драгметаллов"
    Gold = "Передел аффинажа золота"
    Silver = "Передел аффинажа серебра"
    Platinum = "Передел аффинажа платины"
    Rhodium = "Передел аффинажа родия и иридия"
    Recycling = "Передел переработки катализаторов"
    laboratory = "Центральная лаборатория"
    Cleaning = "Участок бытового обслуживания"
    General = "Общий отдел"


class TypeViolation(enum.Enum):
    Access_mode = "Пропускной режим"
    Information_security = "Информационная безопасность"
    Work_schedule = "Трудовой распорядок"



