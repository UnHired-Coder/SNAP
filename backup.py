from  Snap  import db, login_manager
from Snap import db
from datetime import datetime
from flask_login import UserMixin
from Snap import db,login_manager,app



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20),  nullable=False, default='default.jpg')
    image_url = db.Column(db.String(500))
    bio= db.Column(db.String(200)) 
    followers = db.Column(db.Integer)
    following = db.Column(db.Integer)
    no_of_post = db.Column(db.Integer)
    Love = db.Column(db.Integer)
    Link_facebook = db.Column(db.String(120),default='#')
    Link_twitter = db.Column(db.String(120),default='#')
    Link_other = db.Column(db.String(120),default='#')     
    password = db.Column(db.String(40), nullable=False)
   
    post = db.relationship('Post', backref='author', lazy=True)
    
    
    liked = db.relationship(
        'PostLike',
        foreign_keys='PostLike.user_id',
        backref='user', lazy='dynamic')

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
        return f"User('{self.username}','{self.email}','{self.image_file}','{self.image_url}','{self.post}','{self.bio}','{self.followers}','{self.following}','{self.no_of_post}','{self.Love}','{self.Link_facebook}','{self.Link_twitter}','{self.Link_other}')"    


class Post(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    title= db.Column(db.String(100), nullable=False)
    date_posted= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content= db.Column(db.Text)
    post_file= db.Column(db.String(20), nullable=False, default='default.jpg')
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')
    shares= db.Column(db.Integer,default=0)     
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False) 
    tag = db.Column(db.String(50),nullable=False)
    post_comment = db.relationship('Comments', backref='comment_author',lazy='dynamic')            
    
    def make_comment(self,data):
        #comment_by = Post.query.filter(PostLike.user_id == self.id,PostLike.post_id == post.id)       
        newComment = Comments(user_id=self.author.id, post_id=self.id,comment=data)
        db.session.add(newComment)               

     
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}','{self.tag}','{self.post_file}','{self.likes}','{self.shares}','{self.post_comment}')"

    
class Comments(db.Model):
     
    id= db.Column(db.Integer,primary_key=True)
    comment= db.Column(db.String(100))
    comment_by = db.Column(db.String(100))
    post_id= db.Column(db.Integer,db.ForeignKey('post.id'))        
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    

class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    