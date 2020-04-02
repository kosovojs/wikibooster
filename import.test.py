import re


def handleArticleRemoval(newArticles, task, subtask = None, shouldConvertFormat = False):
	taskID = self.db.getTaskID(self.wiki, task, subtask)
	currArticles = self.db.getCurrentArticlesForImport(taskID)
	if shouldConvertFormat:
		newArticles = [[f, self.wiki, taskID] for f in newArticles]
	candidateArticles = [f for f in newArticles if f[0] not in currArticles]

	return candidateArticles
