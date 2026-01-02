import json
from pathlib import Path

from redditreview.core.praw_core import reddit_client


class RedditScrape:
    def __init__(self, search):
        self.reddit = reddit_client()
        self.search = search

    def extract_reddit_posts(self):
        results = self.reddit.subreddit("all").search(
            self.search, sort="relevance", time_filter="year", limit=50
        )
        return results

    def filter_best_posts(self, posts, top_n=10, min_score=20, min_comments=5):
        """Filter and rank posts by engagement."""
        filtered = []
        for post in posts:
            if not post.is_self:
                continue

            if post.score < min_score or post.num_comments < min_comments:
                continue

            # Engagement score: weight score + comments
            engagement = post.score + (post.num_comments * 2)
            filtered.append((post, engagement))

        # Sort by engagement, take top N
        filtered.sort(key=lambda x: x[1], reverse=True)
        return [post for post, _ in filtered[:top_n]]

    def extract_top_comments(self, post, top_n=20, min_score=5):
        """Extract only high-quality comments."""
        post.comments.replace_more(limit=0)
        comments = []

        for comment in post.comments.list():
            # Filter by score and length
            if comment.score < min_score or len(comment.body) < 25:
                continue

            comments.append(
                {
                    "author": str(comment.author) if comment.author else "[deleted]",
                    "body": comment.body,
                    "score": comment.score,
                }
            )

        # Sort by score, take top N
        comments.sort(key=lambda x: x["score"], reverse=True)
        return comments[:top_n]

    def scrape_and_save(self, output_dir="data", top_posts=10, top_comments=20):
        """Scrape best posts with top comments, save compact JSON."""
        posts = self.extract_reddit_posts()
        best_posts = self.filter_best_posts(posts, top_n=top_posts)
        data = []

        for post in best_posts:
            print(f"Extracting from: {post.title}")
            comments = self.extract_top_comments(post, top_n=top_comments)

            post_data = {
                "title": post.title,
                "selftext": post.selftext[:500]
                if len(post.selftext) > 500
                else post.selftext,
                "score": post.score,
                "num_comments": post.num_comments,
                "subreddit": post.subreddit.display_name,
                "url": post.url,
                "top_comments": comments,
            }
            data.append(post_data)

        # Save compact JSON
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        filename = output_path / f"{self.search.replace(' ', '_')}_top_posts.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\nSaved {len(data)} best posts with top comments to {filename}")

        # Print stats
        total_comments = sum(len(p["top_comments"]) for p in data)
        print(f"Total comments saved: {total_comments}")
        print(
            f"Average comments per post: {total_comments / len(data) if data else 0:.1f}"
        )

        return data
