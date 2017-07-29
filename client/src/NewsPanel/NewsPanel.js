import './NewsPanel.css';
import React from 'react';

//import _ from 'lodash';

import NewsCard from '../NewsCard/NewsCard'

class NewsPanel extends React.Component{
    constructor() {
        super();
        this.state = {news:null};
        //this.handleScroll = this.handleScroll.bind(this);
    }

    componentDidMount() {
        this.loadMoreNews();
        //this.loadMoreNews = _.debounce(this.loadMoreNews, 1000);
        //window.addEventListener('scroll', this.handleScroll);
    }

    // handleScroll() {
    //     let scrollY = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;
    //     if ((window.innerHeight + scrollY) >= (document.body.offsetHeight - 50)) {
    //         console.log('Loading more news');
    //         this.loadMoreNews();
    //     }
    // }

    loadMoreNews() {
        let request = new Request('http://localhost:3000/news', {
            method: 'GET',
            //if cache is true, will get same news if refresh
            cache: false});

        fetch(request)
            .then((res) => res.json())
            .then((news) => {
                this.setState({
                    //if this.state.news is not null, add fetched news to existing news and set state
                    news: this.state.news? this.state.news.concat(news) : news,
                });
            });
    }

    renderNews() {
        let news_list = this.state.news.map(function(news) {
            return(
                <a className='list-group-item' key={news.digest} href="#">
                    <NewsCard news={news} />
                </a>
            );
        });

        return(
            <div className="container-fluid">
                <div className='list-group'>
                    {news_list}
                </div>
            </div>
        );
    }

    render() {
        if (this.state.news) {
            return(
                <div>
                    {this.renderNews()}
                </div>
            );
        } else {
            return(
                <div>
                    <div id='msg-app-loading'>
                        Loading
                    </div>
                </div>
            );
        }
    }
}

export default NewsPanel;
