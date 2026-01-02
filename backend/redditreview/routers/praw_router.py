from fastapi import APIRouter
from redditreview.services.praw_service import RedditScrape

router = APIRouter()


@router.post("/scrape")
async def scrape_reddit(search):
    main = RedditScrape(search)
    data = main.scrape_and_save(
        output_dir="/home/banid/projects/RedditReview/backend/redditreview/json",
        top_posts=10,
        top_comments=20,
    )

    # Preview
    for post in data[:2]:
        print(f"\n{'=' * 60}")
        print(f"Title: {post['title']}")
        print(f"Score: {post['score']} | Comments: {post['num_comments']}")
        print(f"Top comments saved: {len(post['top_comments'])}")
        if post["top_comments"]:
            print(
                f"Best comment ({post['top_comments'][0]['score']} pts): {post['top_comments'][0]['body'][:150]}..."
            )
