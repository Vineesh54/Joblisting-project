"use client"; // This is a client component

import axios from 'axios';
import { useEffect, useState } from 'react';

const JobList = () => {
  const [jobs, setJobs] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredJobs, setFilteredJobs] = useState([]);

  // Fetch job data from backend
  useEffect(() => {
    axios.get('http://127.0.0.1:8000/jobs/')
      .then(response => {
        console.log(response.data); // Log the response to inspect its structure
        setJobs(response.data); // Set the jobs state
        setFilteredJobs(response.data); // Initialize filtered jobs with all jobs
      })
      .catch(error => {
        if (error.response) {
          console.error('Backend responded with error:', error.response.data);
        } else if (error.request) {
          console.error('No response received:', error.request);
        } else {
          console.error('Axios error:', error.message);
        }
      });
  }, []);

  // Filter jobs based on search query
  useEffect(() => {
    if (searchQuery.trim() === '') {
      setFilteredJobs(jobs); // If search is empty, show all jobs
    } else {
      setFilteredJobs(
        jobs.filter(job => 
          job.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
          job.company_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
          job.location.toLowerCase().includes(searchQuery.toLowerCase())
        )
      );
    }
  }, [searchQuery, jobs]);

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-extrabold text-center text-gray-900 mb-8">Job Listings</h1>

      {/* Search Box */}
      <div className="mb-6 flex justify-center">
        <input
          type="text"
          placeholder="Search by title, company, or location"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="p-2 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Job Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {filteredJobs.map((job) => (
          <div key={job.id} className="border border-gray-200 p-6 rounded-lg shadow-lg hover:shadow-2xl transition-shadow duration-300 ease-in-out bg-white">
            <h2 className="text-2xl font-semibold text-gray-800 mb-2">{job.title}</h2>
            <p className="text-lg text-gray-600 mb-1">{job.company_name}</p>
            <p className="text-sm text-gray-500 mb-1">{job.location}</p>
            <p className="text-sm text-gray-500 mb-3">{job.posted_date}</p>
            <p className="text-sm text-gray-500 mb-4">{job.employment_type}</p>
            <a
              href={job.details_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block text-blue-500 hover:text-blue-700 font-semibold text-sm"
            >
              View Details
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default JobList;
