const puppeteer = require("puppeteer");
const fs = require("fs");

const authors = [
  "chayapatr",
  "nutn0n",
  "chottiwattj",
  "nick",
  "nithiwat",
  "jirasin",
  "kornkt14",
  "chanud",
  "nisa",
  "kanyarat",
  "ami",
  "Bunkueanun",
  "emmy",
  "mefourth",
  "onosaka",
  "pktonycrux",
  "Prompt",
  "spacezab",
  "unko",
];
const baseURL = "https://spaceth.co/author";

const getPageNum = async (page) => {
  const num = await page.evaluate(
    (element) => element.textContent,
    await page.$(
      "#main > div.s-paging.alignwide.justify-center > *:nth-last-child(2)"
    )
  );
  return num;
};

const getLinks = async (page) => {
  return await Promise.all(
    (
      await page.$$("div.entry-info > h2 > a")
    ).map(async (t) => {
      return await t.evaluate((x) => x.getAttribute("href"));
    })
  );
};

const getPageData = async (page) => {
  const title = await page.evaluate(
    (element) => element.textContent,
    await page.waitForSelector("#main > header > h1")
  );
  const date = await page.evaluate(
    (element) => element.textContent,
    await page.waitForSelector(
      "#main > header > div.entry-meta.single-meta > span > time.entry-date.published"
    )
  );
  const body = await page.evaluate(
    (element) => element.textContent,
    await page.waitForSelector("#main > div.single-content")
  );

  return title + "\n" + date + "\n\n" + body;
};

const createFolder = async (author) => {
  if (!fs.existsSync(`scrape/${author}`)) {
    fs.mkdirSync(`scrape/${author}`, { recursive: true });
  }
  return author;
};

const scrapeAuthor = async (page, author) => {
  await page.goto(`${baseURL}/${author}`);
  let num = 1;

  try {
    num = parseInt(await getPageNum(page));
  } catch {
    console.log("no pages");
  }

  createFolder(author);

  for (let pageNum = 1; pageNum <= parseInt(num); pageNum++) {
    await page.goto(`${baseURL}/${author}/page/${pageNum}`);

    const links = await getLinks(page);

    for (let i = 0; i < links.length; i++) {
      const slug = links[i].split("/").at(-2);

      if (fs.existsSync(`scrape/${author}/${slug}.txt`)) {
        console.log(`skipping ${links[i]}`);
        continue;
      }

      await page.goto(links[i]);
      console.log(`fetch: ${links[i]}`);
      const rawText = await getPageData(page);
      const text = rawText;

      fs.writeFile(`scrape/${author}/${slug}.txt`, text, function (err) {
        if (err) throw err;
        console.log(`write file: ${slug}`);
      });

      await page.goBack();
    }
  }
};

const scrape = async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  for (let i = 0; i < authors.length; i++) {
    const x = await scrapeAuthor(page, authors[i]);
    console.log(x);
  }

  browser.close();
};

scrape();
