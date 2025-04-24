import { useEffect } from 'react';

// Custom hook to insert a script tag on any page the Component is loaded.
// Used primarily to get the google maps api onto our app.
//
// @url = The url of the script you want to load.

const useScript = url => {
  useEffect(() => {
    const script = document.createElement('script');

    script.src = url;
    script.async = true;
    script.defer = true;

    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    }
  }, [url]);
};

export default useScript;
