// This component displays a horizontally scrollable section of blog posts.
// It simulates fetching blog data and displays it in a carousel format.
// In a real application, this would fetch data from an API endpoint.

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './BlogSection.css';

const BlogSection = () => {
  // State for blog posts data
  const [blogPosts, setBlogPosts] = useState([]);
  // Loading state for asynchronous operations
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Simulate API call with mock data
    // In a real application, this would be replaced with an actual API call
    const fetchBlogPosts = () => {
      setLoading(true);
      
      // Mock blog data - this simulates what would come from an API
      // This approach is useful for development and testing before the backend is ready
      const mockBlogPosts = [
        {
          id: 1,
          title: "10 Best Beach Destinations for Your Next Vacation",
          excerpt: "Discover the most beautiful beaches around the world perfect for your next getaway...",
          author: "Travel Expert",
          date: "April 10, 2025",
          category: "Travel Tips",
          imageUrl: "beach-placeholder.jpg"
        },
        {
          id: 2,
          title: "How I Transformed My Spare Room Into a Profitable Rental",
          excerpt: "Learn how I started my hosting journey and turned my guest room into a consistent source of income...",
          author: "Successful Host",
          date: "April 5, 2025",
          category: "Host Stories",
          imageUrl: "room-placeholder.jpg"
        },
        {
          id: 3,
          title: "Sustainable Travel: Eco-Friendly Accommodations on the Rise",
          excerpt: "The growing trend of environmentally conscious travel and how hosts are adapting...",
          author: "Green Travel Advocate",
          date: "March 28, 2025",
          category: "Travel Trends",
          imageUrl: "eco-placeholder.jpg"
        },
        {
          id: 4,
          title: "From Farmhouse to Dream Stay: The Story of Casa Bella",
          excerpt: "How one family renovated a century-old farmhouse into one of our most booked properties...",
          author: "Property Editor",
          date: "March 15, 2025",
          category: "Property Highlights",
          imageUrl: "farmhouse-placeholder.jpg"
        },
        {
          id: 5,
          title: "5 Tips for a Memorable Family Vacation",
          excerpt: "Planning a trip with kids? Here's how to make it enjoyable for everyone...",
          author: "Family Travel Expert",
          date: "March 10, 2025",
          category: "Travel Tips",
          imageUrl: "family-placeholder.jpg"
        },
        {
          id: 6,
          title: "The Rise of Digital Nomad-Friendly Accommodations",
          excerpt: "How properties are adapting to the growing remote work trend...",
          author: "Lifestyle Writer",
          date: "March 5, 2025",
          category: "Travel Trends",
          imageUrl: "nomad-placeholder.jpg"
        }
      ];
      
      // Simulate network delay (500ms) to demonstrate loading state
      // This is a common practice during development to test UI transitions
      setTimeout(() => {
        setBlogPosts(mockBlogPosts);
        setLoading(false);
      }, 500);
    };
    
    fetchBlogPosts();
  }, []); // Empty dependency array means this effect runs once on component mount (refresh of the page)
  
  return (
    <div className="blog-section-container">
      <div className="carousel-container">
        {loading ? (
          // Show loading message while data is being "fetched"
          <p className="loading-message">Loading blog posts...</p>
        ) : (
          // Display blog carousel once data is loaded
          <div className="blog-carousel">
            {blogPosts.map(post => (
              <div className="blog-card" key={post.id}>
                <div className="blog-image">
                  {/* Placeholder for blog image */}
                  <div className="blog-placeholder-image"></div>
                  <div className="blog-category">{post.category}</div>
                </div>
                <div className="blog-content">
                  <h3 className="blog-title">{post.title}</h3>
                  <p className="blog-excerpt">{post.excerpt}</p>
                  <div className="blog-meta">
                    <span className="blog-author">{post.author}</span>
                    <span className="blog-date">{post.date}</span>
                  </div>
                  {/* Link to individual blog post - would be implemented in a real app */}
                  <Link to={`/blog/${post.id}`} className="read-more-btn">
                    Read More
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      {/* Link to full blog page */}
      <div className="view-all-container">
        <Link to="/blog" className="view-all-btn">View All Articles</Link>
      </div>
    </div>
  );
};

export default BlogSection;