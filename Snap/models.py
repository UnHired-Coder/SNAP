from  Snap  import db, login_manager
from Snap import db
from datetime import datetime
from flask_login import UserMixin
from Snap import db,login_manager,app
from flask_msearch import Search
from flask_login import current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    __tablename__= 'user'
    __searchable__= ['username']

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    image_file = db.Column(db.String(20),  nullable=False, default='default.jpg')
    image_url = db.Column(db.String(500))
    bio= db.Column(db.String(200))

    following_to = db.relationship('Following_to',backref='to_author', lazy='dynamic')
    # following_by = db.relationship('Following_by',backref='by_author', lazy='dynamic')

    Link_facebook = db.Column(db.String(120),default='#')
    Link_twitter = db.Column(db.String(120),default='#')
    Link_other = db.Column(db.String(120),default='#')

    post = db.relationship('Post', backref='author', lazy=True)


    def isfollowingto(self, userid):
        return Following_to.query.filter(Following_to.from_user_id == self.id,
                                        Following_to.to_user == userid ).count()>0
     
    def following_by_count(self, userid):
        return Following_to.query.filter_by(
                to_user=userid,
                ).count()
    
    def following_to_count(self, userid):
        return Following_to.query.filter_by(
                from_user_id=userid,
                ).count()

    def follow_user(self, user):
        if not self.isfollowingto(user):
            userr = Following_to(from_user_id=self.id, to_user=user)
            db.session.add(userr)

    def unfollow_user(self, user):
        if  self.isfollowingto(user):
            user = Following_to.query.filter_by(
            from_user_id=self.id,
            to_user=user).delete()


    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}','{self.image_url}','{self.post}','{self.bio}','{self.following_to}','{self.following_by}','{self.Link_facebook}','{self.Link_twitter}','{self.Link_other}')"

class Following_to(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    from_user_id= db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    to_user= db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Following_to('{self.from_user_id}','{self.to_user}')"

# class Following_by(db.Model):
#     id= db.Column(db.Integer,primary_key=True)
#     to_user= db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
#     from_user_id= db.Column(db.Integer, nullable=False)

#     def __repr__(self):
#         return f"Following_by('{self.from_user_id}','{self.to_user}')"

class Post(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'))
    title= db.Column(db.String(100), nullable=False)
    date_posted= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content= db.Column(db.Text)
    post_file= db.Column(db.String(20), nullable=False, default='default.jpg')
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')
    shares= db.Column(db.Integer,default=0)
    tag = db.Column(db.String(50),nullable=False)
    post_comment = db.relationship('Comments', backref='comment_author',lazy='dynamic')

    def make_comment(self,data, author):
        newComment = Comments(author_name = author,user_id = current_user.id, post_id=self.id,comment=data)
        db.session.add(newComment)

    def post_comment_list(self, post):
        return Comments.query.filter(

            Comments.post_id == post.id).all()


    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}','{self.tag}','{self.post_file}','{self.likes}','{self.shares}','{self.post_comment}')"


class Comments(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    comment= db.Column(db.String(100))
    author_name = db.Column(db.String(20), nullable=False)
    post_id= db.Column(db.Integer,db.ForeignKey('post.id'))
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))


class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
