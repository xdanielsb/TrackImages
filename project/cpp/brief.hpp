#include <opencv2/nonfree/features2d.hpp>

vp2 briefI(Mat trainingImg, Mat frame1) {

	auto detector = FeatureDetector::create("BRIEF");

	//var to storage
	vkp kpObject, kpScene;

	//detect the key points
	detector->detect(trainingImg, kpObject);
	detector->detect(frame1, kpScene);

	//detect the descriptors
	auto extractor = DescriptorExtractor::create("BRIEF");
	Mat descObject, descScene;

	extractor->compute(trainingImg, kpObject, descObject);
	extractor->compute(frame1, kpScene, descScene);

	//Matching the descriptors using FLANN matcher

	auto matcher = DescriptorMatcher::create("BRIEF");
	vdm1 matches;
	matcher->match(descObject, descScene, matches);
	double maxDistance = 0, minDistance = 500;

	//Compute the max and the min distance
	for (int i = 0; i < descObject.rows; i++) {
		double dist = matches[i].distance;
		if (dist < minDistance)
			minDistance = dist;
		if (dist > maxDistance)
			maxDistance = dist;
	}

	//	printf("Max distance: %f  \n", maxDistance);
	//	printf("Min distance: %f  \n", minDistance);

	//Draw the good matches
	//printf("sift: The number of matches is %d \n", matches.size());
	vdm2 goodMatches;
	for (int i = 0; i < descObject.rows; i++) {
		double dist = matches[i].distance;
		if (dist < 3 * minDistance)
			goodMatches.push(DMatch2(matches[i], dist));
	}
	vp2 points;
	while (!goodMatches.empty()) {
		DMatch2 aux = goodMatches.top();
		goodMatches.pop();
		Point2f a = kpScene[aux.dm.trainIdx].pt;
		//Point2f b = kpScene[aux.queryIdx].pt;
		points.pb(a);
	}

	return points;
}
