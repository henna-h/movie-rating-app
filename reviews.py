from db import db

def get_reviews_by_user(id):
    sqlReviews = "SELECT * FROM reviews WHERE user_id=:user_id ORDER BY submitted_at DESC"
    resultReviews = db.session.execute(sqlReviews, {"user_id":id})
    reviews = resultReviews.fetchall()

    return reviews

def get_reviews_by_movie(id):
    sqlReviews = "SELECT * FROM reviews WHERE movie_id=:movie_id ORDER BY submitted_at DESC"
    resultReviews = db.session.execute(sqlReviews, {"movie_id":id})
    reviews = resultReviews.fetchall()

    return reviews

def get_users_review_count(id):
    sqlReviewCount = "SELECT COUNT(*) FROM reviews WHERE user_id=:user_id"
    resultReviewCount = db.session.execute(sqlReviewCount, {"user_id":id})
    reviewCount = resultReviewCount.fetchone()[0]

    return reviewCount

def get_movies_review_count(id):
    sqlReviewCount = "SELECT COUNT(*) FROM reviews WHERE movie_id=:movie_id"
    resultReviewCount = db.session.execute(sqlReviewCount, {"movie_id":id})
    reviewCount = resultReviewCount.fetchone()[0]

    return reviewCount

def add_review(stars, review, user_id, movie_id):
    sqlReview = "INSERT INTO reviews (stars, review, movie_id, user_id) VALUES (:stars, :review, :movie_id, :user_id)"
    db.session.execute(sqlReview, {"stars":stars, "review":review, "movie_id":movie_id, "user_id":user_id})
    db.session.commit()

def delete_review(id):
    sql="DELETE FROM reviews WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()