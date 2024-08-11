import { useEffect, useState } from 'react';

const useSSE = (url, eventType) => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const eventSource = new EventSource(url);

    eventSource.onmessage = (event) => {
      const parsedData = JSON.parse(event.data);
      if (parsedData.type === eventType) {
        setData(parsedData);
      }
    };

    return () => {
      eventSource.close();
    };
  }, [url, eventType]);

  return data;
};

export default useSSE;
