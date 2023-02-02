### Russia-Ukraine Discourse on Twitter Surrounding Significant Conflict Events

A project of the Irregular Warfare and Conflict Analysis Group (IWCAG) of the National Consortium for the Study of Terrorism and Responses to Terrorism (START) at the University of Maryland, College Park.

#### Set Up
This repository uses [pipenv](https://github.com/pypa/pipenv) for environment and package management. It requires [Python 3.11](https://www.python.org/downloads/)
. 
For setup, first install pipenv with pip:

```bash
pip install pipenv
```

Then, to load the environment from the `Pipfile` and `Pipfile.lock`, run:

```bash
pipenv install
```

You can then activate the environment from the working directory with:

```bash
pipenv shell
```

#### A Note on Telegram

Use Bellingcat's [fork of snscrape](https://github.com/bellingcat/snscrape) for expanded Telegram capabilities pending [merge of Bellingcat's changes](https://github.com/JustAnotherArchivist/snscrape/pull/413) into the official snscrape library.

### TODO:

[x] Add Telegram support.
[x] Add Weibo support.
[ ] Package scripts into a class object.

---

### Battles

| event_id | event                                        | start     | end       | victor  |
|----------|----------------------------------------------|-----------|-----------|---------|
| b01      | Battle of Kherson                            | 2/24/2022 | 3/2/2022  | Russia  |
| b02      | Battle of Kharkiv                            | 2/24/2022 | 5/14/2022 | Ukraine |
| b03      | Battle of Kyiv                               | 2/25/2022 | 4/2/2022  | Ukraine |
| b04      | Siege of Mariupol                            | 2/24/2022 | 5/20/2022 | Russia  |
| b05      | Battle of Melitopol                          | 2/25/2022 | 3/1/2022  | Russia  |
| b06      | The Battle of Sievierodonetsk and Lysychansk | 5/6/2022  | 6/25/2022 | Russia  |
| b07      | Battle of Chernihiv                          | 2/24/2022 | 4/4/2022  | Ukraine |
| b08      | Battle of Lysychansk                         | 6/25/2022 | 7/3/2022  | Russia  |
| b09      | Battle of Donets                             | 5/5/2022  | 5/13/2022 | Ukraine |

### Civilian Events

| event_id | event                                 | date      | targettype   | civiliandeath |
|----------|---------------------------------------|-----------|--------------|---------------|
| civ01    | Mariupol materinity hospital attack   | 3/9/2022  | healthcare   | 3             |
| civ02    | Mariupol theater bombing              | 3/16/2022 | relig/cult   | 600           |
| civ03    | Chernikiv attack on bread queue       | 3/16/2022 | shopping     | 10            |
| civ04    | Merefa school/community center attack | 3/17/2022 | school       | 21            |
| civ05    | Bucha massacre                        | 4/4/2022  | execution    | 400           |
| civ06    | Mykolaiv children's hospital          | 4/5/2022  | healthcare   | 2             |
| civ07    | Kramatorks train station attack       | 4/8/2022  | transportat  | 52            |
| civ08    | Skovoroda musuem attack               | 5/6/2022  | relig/cult   | 0             |
| civ09    | Bilohorivka school  attack            | 5/8/2022  | school       | 60            |
| civ10    | Lozova's Palace of Culture attack     | 5/20/2022 | relig/cult   | 0             |
| civ11    | Svyatohirsk Lavra monastery attack    | 6/4/2022  | relig/cult   | 0             |
| civ12    | Kremenchuk mall attack                | 6/27/2022 | shopping     | 20            |
| civ13    | Vinnytysia business center attack     | 7/15/2022 | businesscntr | 23            |
| civ14    | Peremoha post office massacle         | 7/25/2022 | execution    | 5             |

### Non-English Terms
Terms from [echen102](https://github.com/echen102)'s [Ukraine and Russia Conflict Tweet IDs Dataset](https://github.com/echen102/ukraine-russia).

**Google Translate**
| Non-English    | English                    |
|----------------|----------------------------|
| Украина        | Ukraine                    |
| украины        | Ukraine                    |
| Україна        | Ukraine                    |
| Киев           | Kiev                       |
| Київ           | Kyiv                       |
| Россия         | Russia                     |
| Донбасс        | Donbass                    |
| ФСБ            | FSB                        |
| КГБ            | KGB                        |
| кгб            | KGB                        |
| своихнебросаем | "We don't abandon our own" |
