import shutil
import os
import copy

def eraseFiles(path):
    for file in os.listdir(path):
        filePath = os.path.join(path, file)
        try:
            shutil.rmtree(filePath)
        except OSError:
            os.remove(filePath)

class Export():
    def __init__(self, singleTemplatesPath, singleExportPath, allTemplatesPath, allExportPath, bannedTemplate, errorTemplate):
        self.singleTemplatesPath = singleTemplatesPath
        self.singleExportPath = singleExportPath
        self.singleTemplates = []

        for file in os.listdir(self.singleTemplatesPath):
            if file.endswith(".txt"):
                self.singleTemplates.append(file)

        self.allTemplatesPath = allTemplatesPath
        self.allExportPath = allExportPath
        self.allTemplates = []

        for file in os.listdir(self.allTemplatesPath):
            if file.endswith(".txt"):
                try:
                    path = os.path.join(self.allExportPath, str(file).split(".")[0])
                    os.mkdir(path)
                except Exception:
                    pass
                self.allTemplates.append(file)
        
        self.bannedTemplate = bannedTemplate
        self.errorTemplate = errorTemplate

    def exportSingle(self, accounts):
        for template in self.singleTemplates:
            with open(f"{self.singleTemplatesPath}\{template}", "r", encoding="utf-8", newline="") as filePointer:
                fileData = filePointer.read()
                with open(f"{self.singleExportPath}\{template}", "a+", encoding="utf-8", newline="") as exportPointer:
                    for account in accounts:
                        if account["state"] == "OK":
                            data = copy.copy(fileData)
                        elif account["state"] == "BANNED":
                            data = copy.copy(self.bannedTemplate)
                        else:
                            data = copy.copy(self.errorTemplate)

                        for key, value in account.items():
                            data = data.replace(f"{{{key}}}", str(value))

                        exportPointer.write(data + "\n")

    def exportAll(self, accounts):
        for template in self.allTemplates:
            with open(f"{self.allTemplatesPath}\{template}", "r", encoding="utf-8", newline="") as filePointer:
                fileData = filePointer.read()
                for account in accounts:
                        if account["state"] == "OK":
                            data = copy.copy(fileData)
                        elif account["state"] == "BANNED":
                            data = copy.copy(self.bannedTemplate)
                        else:
                            data = copy.copy(self.errorTemplate)

                        for key, value in account.items():
                            data = data.replace(f"{{{key}}}", str(value))

                        with open(f"{self.allExportPath}\{str(template).split('.')[0]}\{account['username']}.txt", "w", encoding="utf-8", newline="") as exportPointer:
                            exportPointer.write(data + "\n")

def exportAccounts(accounts, bannedTemplate, errorTemplate):
    export = Export("templates\\single", "export\\single", "templates\\all", "export\\all", bannedTemplate, errorTemplate)
    export.exportSingle(accounts)
    export.exportAll(accounts)

